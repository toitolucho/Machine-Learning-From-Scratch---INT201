# Proyectos – Segundo Parcial INT201 (Machine Learning aplicado a ciberseguridad)

## Estructura

```
proyectos/
├── plantillas/
│   ├── plantilla_enunciado_estudiante.md   ← enunciado académico (lo que recibe el estudiante)
│   ├── bitacora_decisiones.md              ← registro de decisiones del estudiante
│   ├── plantilla_guia_docente.md           ← problemas incorporados, solución y rúbrica
│   └── plantilla_defensa_oral.md           ← preguntas y tareas en vivo con respuesta esperada
└── P01_logins_sospechosos/                 ← proyecto de muestra
    ├── estudiante/   ← ENTREGAR: enunciado.md, bitacora_decisiones.md, data/
    └── docente/      ← NO ENTREGAR: guía, notebook de solución, defensa oral, generadores
```

## Componentes de cada proyecto

| Componente | Para quién | Propósito |
|---|---|---|
| Enunciado | Estudiante | Caso, restricciones, diccionario de datos, hipótesis, actividades y criterios, en tercera persona |
| Conjunto de datos | Estudiante | Datos con problemas de calidad incorporados intencionalmente; cada uno tiene una pista en el enunciado |
| Bitácora de decisiones | Estudiante | Registro de cada decisión con su evidencia; base de la defensa oral |
| Guía docente | Docente | Problemas incorporados, pistas, resultados de referencia, hipótesis resueltas y rúbrica |
| Notebook de solución | Docente | Desarrollo paso a paso con el formato Decisión → Evidencia → Justificación |
| Defensa oral | Docente | Preguntas por bloques y tareas en vivo sobre el notebook, con la respuesta esperada |

## Regenerar un proyecto

```bash
cd P01_logins_sospechosos/docente
python generar_datos.py
python construir_notebook_solucion.py
```
