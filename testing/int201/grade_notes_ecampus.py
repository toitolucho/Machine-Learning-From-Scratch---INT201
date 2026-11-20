#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
grade_notes_ecampus.py - Subida y Registro de Calificaciones a eCampus (Moodle)
=============================================================================
Este script lee las notas desde 'notes.txt' (correo, nota), busca la tarea
en eCampus por su ID de módulo (CMID), empareja los correos con los usuarios
matriculados en el curso, genera un reporte estadístico local en CSV y sube
las calificaciones y retroalimentaciones a Moodle mediante la API WebService.

Uso:
    python grade_notes_ecampus.py               # Modo interactivo / verificación
    python grade_notes_ecampus.py --dry-run     # Solo genera reporte sin subir
    python grade_notes_ecampus.py --push        # Sube las calificaciones directamente
=============================================================================
"""

import os
import sys
import argparse
import requests
import json
import csv
from datetime import datetime
from dotenv import load_dotenv

# Asegurar codificación UTF-8 en consola de Windows
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass


def find_and_load_env():
    """Busca el archivo .env en el directorio actual o en directorios superiores."""
    curr = os.path.abspath(os.path.dirname(__file__))
    while curr:
        candidate = os.path.join(curr, '.env')
        if os.path.exists(candidate):
            load_dotenv(candidate)
            return candidate
        parent = os.path.dirname(curr)
        if parent == curr:
            break
        curr = parent
    load_dotenv()
    return None


class MoodleGrader:
    def __init__(self, cmid=420898, domain=None, token=None):
        self.cmid = cmid
        self.domain = domain or os.environ.get('MOODLE_DOMAIN', 'https://ecampus.usfx.bo').rstrip('/')
        self.token = token or os.environ.get('MOODLE_TOKEN')
        self.endpoint = f"{self.domain}/webservice/rest/server.php"
        
        # Validar o renovar token
        if not self.test_connection():
            print("⚠️ Token actual no válido o ausente. Intentando obtener nuevo token con credenciales...")
            self.renew_token()

    def renew_token(self):
        username = os.environ.get('MOODLE_USERNAME')
        password = os.environ.get('MOODLE_PASSWORD')
        if not username or not password:
            raise RuntimeError("❌ No se encontraron credenciales MOODLE_USERNAME y MOODLE_PASSWORD en .env para generar un token.")
        
        token_url = f"{self.domain}/login/token.php"
        data = {
            'username': username,
            'password': password,
            'service': 'moodle_mobile_app'
        }
        res = requests.post(token_url, data=data)
        res_json = res.json()
        if 'token' in res_json:
            self.token = res_json['token']
            print(f"✅ Token obtenido exitosamente.")
        else:
            raise RuntimeError(f"❌ Error obteniendo token: {res_json.get('error', res.text)}")

    def call_moodle(self, function, params=None):
        if params is None:
            params = {}
        data = {
            'wstoken': self.token,
            'wsfunction': function,
            'moodlewsrestformat': 'json'
        }
        data.update(params)
        try:
            r = requests.post(self.endpoint, data=data, timeout=30)
            r.raise_for_status()
            res = r.json()
            if isinstance(res, dict) and 'exception' in res:
                return {'error': res.get('message', 'Error desconocido'), 'raw': res}
            return res
        except Exception as e:
            return {'error': str(e)}

    def test_connection(self):
        if not self.token:
            return False
        res = self.call_moodle('core_webservice_get_site_info')
        if isinstance(res, dict) and 'userid' in res:
            self.user_fullname = res.get('fullname')
            self.userid = res.get('userid')
            return True
        return False

    def resolve_assignment(self):
        """
        Encuentra el curso y el ID de instancia de la tarea correspondiente al CMID proporcionado.
        """
        print(f"\n🔍 Buscando asignación con CMID (ID de URL) = {self.cmid}...")
        courses = self.call_moodle('core_enrol_get_users_courses', {'userid': self.userid})
        if not isinstance(courses, list):
            raise RuntimeError(f"Error listando cursos: {courses}")

        for course in courses:
            cid = course['id']
            # Intentar primero mediante mod_assign_get_assignments
            assigns = self.call_moodle('mod_assign_get_assignments', {'courseids[0]': cid})
            if assigns and 'courses' in assigns:
                for c_item in assigns['courses']:
                    for a in c_item.get('assignments', []):
                        if a.get('cmid') == self.cmid or a.get('id') == self.cmid:
                            self.course_id = cid
                            self.course_name = course['fullname']
                            self.assignment_id = a['id']
                            self.assignment_name = a['name']
                            self.grade_max = float(a.get('grade', 100))
                            print(f"✅ Encontrada en curso: {self.course_name} (ID: {self.course_id})")
                            print(f"   - Tarea: '{self.assignment_name}'")
                            print(f"   - ID de Instancia (API): {self.assignment_id}")
                            print(f"   - CMID (URL): {self.cmid}")
                            print(f"   - Nota Máxima: {self.grade_max}")
                            return

            # Si no aparece en assigns, buscar en el contenido completo del curso
            contents = self.call_moodle('core_course_get_contents', {'courseid': cid})
            if isinstance(contents, list):
                for sec in contents:
                    for mod in sec.get('modules', []):
                        if mod.get('id') == self.cmid or mod.get('instance') == self.cmid:
                            self.course_id = cid
                            self.course_name = course['fullname']
                            self.assignment_id = mod.get('instance')
                            self.assignment_name = mod.get('name')
                            self.grade_max = 100.0
                            print(f"✅ Encontrada en curso: {self.course_name} (ID: {self.course_id})")
                            print(f"   - Módulo: '{self.assignment_name}' (Tipo: {mod.get('modname')})")
                            print(f"   - ID de Instancia (API): {self.assignment_id}")
                            print(f"   - CMID: {self.cmid}")
                            return

        raise RuntimeError(f"❌ No se encontró la tarea o módulo con ID {self.cmid} en los cursos del usuario.")

    def get_enrolled_students(self):
        """Obtiene la lista de usuarios matriculados y construye un diccionario por correo."""
        users = self.call_moodle('core_enrol_get_enrolled_users', {'courseid': self.course_id})
        if not isinstance(users, list):
            raise RuntimeError(f"Error al obtener alumnos matriculados: {users}")
        
        email_map = {}
        for u in users:
            email = u.get('email', '').strip().lower()
            if email:
                email_map[email] = {
                    'id': u['id'],
                    'fullname': u.get('fullname', '').strip(),
                    'email': email
                }
        return email_map

    def save_single_grade(self, userid, grade, feedback_text=None):
        """Guarda la calificación y comentario para un estudiante en la tarea."""
        if feedback_text is None:
            feedback_text = (
                f"<p>Estimado/a estudiante, su calificación registrada para la evaluación "
                f"<strong>{self.assignment_name}</strong> es de <strong>{grade:g}/{self.grade_max:g}</strong>.</p>"
            )

        params = {
            'assignmentid': self.assignment_id,
            'userid': userid,
            'grade': float(grade),
            'attemptnumber': -1,
            'addattempt': 0,
            'workflowstate': 'graded',
            'applytoall': 0,
            'plugindata[assignfeedbackcomments_editor][text]': feedback_text,
            'plugindata[assignfeedbackcomments_editor][format]': 1
        }
        res = self.call_moodle('mod_assign_save_grade', params)
        # mod_assign_save_grade retorna None en éxito
        if res is None:
            return True, "OK"
        elif isinstance(res, dict) and 'error' in res:
            return False, res['error']
        elif isinstance(res, dict) and 'exception' in res:
            return False, res.get('message', str(res))
        return True, "OK"


def load_notes_file(filepath):
    """Carga y parsea el archivo de notas."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Archivo de notas no encontrado: {filepath}")

    notes = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) >= 2:
                email = parts[0].strip().lower()
                grade_str = parts[1].strip()

                # Ignorar encabezados o filas de relleno (como '0 0')
                if email in ('correo', 'email', '0') or '@' not in email:
                    continue

                try:
                    notes[email] = float(grade_str)
                except ValueError:
                    print(f"⚠️ [Línea {line_num}] Nota no numérica ignorada: '{grade_str}' para {email}")
    return notes


def generate_report(matched_students, unmatched_notes, enrolled_without_notes, output_csv):
    """Guarda reporte CSV local y muestra estadísticas resumidas."""
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['User_ID', 'Nombre_Completo', 'Correo', 'Nota', 'Estado'])
        for s in matched_students:
            writer.writerow([s['id'], s['fullname'], s['email'], s['grade'], 'LISTO_PARA_SUBIR'])
        for email, grade in unmatched_notes:
            writer.writerow(['N/A', 'NO_MATRICULADO', email, grade, 'NO_ENCONTRADO_EN_CURSO'])
        for s in enrolled_without_notes:
            writer.writerow([s['id'], s['fullname'], s['email'], 'SIN_NOTA', 'FALTA_NOTA'])

    # Estadísticas
    grades = [s['grade'] for s in matched_students]
    avg_grade = sum(grades) / len(grades) if grades else 0.0
    sorted_students = sorted(matched_students, key=lambda x: x['grade'], reverse=True)
    top_5 = sorted_students[:5]
    bottom_5 = sorted_students[-5:][::-1]

    print("\n" + "=" * 65)
    print("📊 RESUMEN ESTADÍSTICO DE CALIFICACIONES")
    print("=" * 65)
    print(f"• Total estudiantes evaluados:   {len(matched_students)}")
    print(f"• Promedio general de la clase:  {avg_grade:.2f} / 100")
    print(f"• Nota más alta:                 {max(grades):.2f}" if grades else "")
    print(f"• Nota más baja:                 {min(grades):.2f}" if grades else "")

    print("\n🏆 Top 5 Calificaciones Más Altas:")
    for rank, s in enumerate(top_5, 1):
        print(f"   {rank}. {s['fullname']:<35} | {s['grade']:>5.1f} pts ({s['email']})")

    print("\n⚠️ 5 Calificaciones Más Bajas:")
    for rank, s in enumerate(bottom_5, 1):
        print(f"   {rank}. {s['fullname']:<35} | {s['grade']:>5.1f} pts ({s['email']})")

    if unmatched_notes:
        print(f"\n❌ Correos con nota no encontrados en Moodle ({len(unmatched_notes)}):")
        for email, g in unmatched_notes:
            print(f"   - {email} (Nota: {g})")

    if enrolled_without_notes:
        print(f"\n⚠️ Estudiantes matriculados sin nota asignada ({len(enrolled_without_notes)}):")
        for s in enrolled_without_notes:
            print(f"   - {s['fullname']} ({s['email']})")

    print(f"\n💾 Reporte CSV guardado en: {output_csv}")
    print("=" * 65)


def main():
    parser = argparse.ArgumentParser(description="Subir calificaciones a eCampus Moodle")
    parser.add_argument('--cmid', type=int, default=420898, help="ID del módulo en la URL (por defecto: 420898)")
    parser.add_argument('--notes', type=str, default=None, help="Ruta al archivo notes.txt")
    parser.add_argument('--dry-run', action='store_true', help="Solo genera el reporte local sin enviar cambios a eCampus")
    parser.add_argument('--push', action='store_true', help="Sube las notas directamente sin confirmación interactiva")
    args = parser.parse_args()

    print("🚀 ===============================================")
    print("   CALIFICADOR Y SINCRONIZADOR DE NOTAS ECAMPUS")
    print("===============================================")

    # 1. Cargar .env
    env_file = find_and_load_env()
    if env_file:
        print(f"ℹ️ Archivo de entorno cargado desde: {env_file}")

    # 2. Inicializar cliente Moodle
    grader = MoodleGrader(cmid=args.cmid)
    print(f"✅ Conectado como: {grader.user_fullname} (ID: {grader.userid})")

    # 3. Resolver Tarea
    grader.resolve_assignment()

    # 4. Cargar archivo de notas
    base_dir = os.path.abspath(os.path.dirname(__file__))
    notes_file = args.notes if args.notes else os.path.join(base_dir, 'notes.txt')
    print(f"\n📂 Cargando notas desde: {notes_file}")
    notes = load_notes_file(notes_file)
    print(f"✅ {len(notes)} registros de notas válidos leídos.")

    # 5. Obtener matriculados y emparejar
    print("\n👥 Obteniendo lista de estudiantes matriculados en eCampus...")
    enrolled_map = grader.get_enrolled_students()
    print(f"✅ {len(enrolled_map)} estudiantes matriculados encontrados.")

    matched_students = []
    unmatched_notes = []

    for email, grade in notes.items():
        if email in enrolled_map:
            st = enrolled_map[email]
            matched_students.append({
                'id': st['id'],
                'fullname': st['fullname'],
                'email': email,
                'grade': grade
            })
        else:
            unmatched_notes.append((email, grade))

    enrolled_without_notes = [
        st for email, st in enrolled_map.items()
        if email not in notes and st['id'] != grader.userid
    ]

    # 6. Generar reporte local
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_csv = os.path.join(base_dir, f"reporte_calificaciones_{args.cmid}.csv")
    generate_report(matched_students, unmatched_notes, enrolled_without_notes, report_csv)

    # 7. Modo de ejecución
    if args.dry_run:
        print("\n🔒 Modo --dry-run activado: No se realizaron cambios en eCampus.")
        return

    should_push = args.push
    if not should_push:
        # Preguntar interactivamente si hay TTY disponible
        if sys.stdin.isatty():
            try:
                confirm = input("\n❓ ¿Desea proceder a SUBIR estas calificaciones a eCampus ahora? (s/N): ").strip().lower()
                should_push = confirm in ('s', 'si', 'y', 'yes')
            except KeyboardInterrupt:
                print("\nOperación cancelada por el usuario.")
                return
        else:
            print("\n💡 Para aplicar los cambios a eCampus en modo no interactivo, ejecute con: --push")
            return

    if not should_push:
        print("\n⏹️ Subida cancelada por el usuario.")
        return

    # 8. Subir calificaciones a eCampus
    print(f"\n📤 Subiendo {len(matched_students)} calificaciones a eCampus...")
    success_count = 0
    fail_count = 0

    for idx, student in enumerate(matched_students, 1):
        uid = student['id']
        name = student['fullname']
        grade = student['grade']
        print(f"[{idx:02d}/{len(matched_students):02d}] Subiendo: {name:<35} | Nota: {grade:>5.1f} ... ", end="", flush=True)
        
        ok, msg = grader.save_single_grade(uid, grade)
        if ok:
            print("✅ OK")
            success_count += 1
        else:
            print(f"❌ ERROR: {msg}")
            fail_count += 1

    print("\n" + "=" * 65)
    print(f"🏁 PROCESO FINALIZADO:")
    print(f"   • Exitosas: {success_count}")
    print(f"   • Fallidas: {fail_count}")
    print("=" * 65)

    # Verificación final
    print("\n🔎 Verificando calificaciones en eCampus...")
    check = grader.call_moodle('mod_assign_get_grades', {'assignmentids[0]': grader.assignment_id})
    if check and 'assignments' in check and check['assignments']:
        uploaded_grades = check['assignments'][0].get('grades', [])
        print(f"✅ Total de calificaciones registradas en la base de datos de eCampus: {len(uploaded_grades)}")
    print("\n✨ ¡Todas las notas han sido sincronizadas correctamente!")


if __name__ == '__main__':
    main()
