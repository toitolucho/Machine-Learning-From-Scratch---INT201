import csv

report_csv_path = r"d:\Documents\USFX\INT210\Machine-Learning-From-Scratch---INT210\testing\reporte_calificaciones_parte1.csv"

with open(report_csv_path, "r", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

print(f"{'ID':<7} | {'Estudiante':<32} | {'Inicio':<8} | {'Entrega':<8} | {'Duracion':<8} | {'Resueltos':<9} | {'Nota':<6} | {'Penal':<6} | {'Final':<6} | {'Penalizado':<10}")
print("-" * 115)

for r in rows:
    t_ini = r['Hora_Inicio'].split(' ')[1] if ' ' in r['Hora_Inicio'] else r['Hora_Inicio']
    t_end = r['Hora_Entrega'].split(' ')[1] if ' ' in r['Hora_Entrega'] else r['Hora_Entrega']
    dur = f"{r['Duracion_Min']}m"
    res = r['Ejercicios_Resueltos']
    base = r['Nota_Base_100']
    pen = r['Total_Penalizaciones_Pts']
    fin = r['Nota_Final_100']
    flag = r['Debe_Penalizarse']
    print(f"{r['User_ID']:<7} | {r['Estudiante']:<32} | {t_ini:<8} | {t_end:<8} | {dur:<8} | {res:<9} | {base:<6} | {pen:<6} | {fin:<6} | {flag:<10}")

print("\n" + "="*80)
print("DETALLE DE ESTUDIANTES PENALIZADOS:")
print("="*80)
for r in rows:
    if r['Debe_Penalizarse'] == 'SI':
        print(f"\n* [{r['User_ID']}] {r['Estudiante']}:")
        print(f"  - Nota Base: {r['Nota_Base_100']} -> Nota Final: {r['Nota_Final_100']} (-{r['Total_Penalizaciones_Pts']} pts)")
        print(f"  - Motivo: {r['Motivo_Penalizacion']}")
