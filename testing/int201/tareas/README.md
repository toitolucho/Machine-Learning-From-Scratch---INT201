# Sistema de Descarga y Calificación Automatizada de Tareas eCampus
**Curso:** Machine Learning - INT210 (Curso ID: 6726)  
**Docente:** Ing. Luis Antonio Molina Yampa  
**Directorio de Trabajo:** `d:\Documents\USFX\INT210\Machine-Learning-From-Scratch---INT210\testing\int201\tareas`

---

## 1. Asignaciones Evaluadas

1. **T01 - WBCD y Evaluación Multimodelo:**
   - **Enlace Moodle:** [INT210MOL: T01 -](https://ecampus.usfx.bo/mod/assign/view.php?id=420907)
   - **CMID:** `420907` | **Instancia API:** `77380`
   - **Tema:** Clasificación diagnóstica de Cáncer de Mama (Wisconsin Diagnostic Breast Cancer - WBCD).
   - **Contenido del Notebook:** Preprocesamiento de diagnosis (`M=1`, `B=0`), separación $X/y$, `train_test_split`, escalamiento estricto con `StandardScaler` (evitando data leakage con `.fit_transform` en train y `.transform` en test), modelado con `KNeighborsClassifier(n_neighbors=5)` y `DecisionTreeClassifier(max_depth=4)`, cálculo de matrices de confusión, y fundamentación teórica del Error Tipo II (Falso Negativo) e invarianza de escala en árboles.

2. **T02 - Taller Comparativo de Clasificadores:**
   - **Enlace Moodle:** [INT210MOL: T02 -](https://ecampus.usfx.bo/mod/assign/view.php?id=420908)
   - **CMID:** `420908` | **Instancia API:** `77381`
   - **Tema:** Torneo y Fronteras de Decisión en dataset *Wine* (`scikit-learn`).
   - **Contenido del Notebook:** Código base del taller guiado (k-NN, Árbol y Naive Bayes con Alcohol y Flavonoides) + Reto Autónomo:
     - *Variante A (Mayoritaria):* Mapa de calor de correlaciones (`sns.heatmap`), identificación de la 3ra característica más representativa (Prolina, Fenoles, etc.), visualización de pares (pairplot/scatter), modelado 2D y representación gráfica de fronteras de decisión (`DecisionBoundaryDisplay`).
     - *Variante B (Alternativa):* Implementación de Regresión Logística con datos escalados y comparación gráfica de fronteras en cuadrícula 2x2 de 4 paneles.

---

## 2. Estructura de Archivos Creados

```text
testing/int201/tareas/
├── download_tareas.py                # Script de conexión, inspección y descarga masiva desde eCampus
├── grade_assignments_int210.py       # Motor principal de calificación, generación de reportes y subida a eCampus
├── inspect_assignments_content.py    # Auditoría inicial de notebooks y extracción de zips
├── scan_submissions.py              # Detección de tipos de contenido y cruce de archivos intercambiados
├── README.md                         # Documentación técnica y resumen pedagógico
├── tarea_420907_inst_77380/         # Directorio con todas las entregas descargadas de T01
│   ├── submissions_summary.json     # Metadatos de alumnos y estado de entrega T01
│   └── User_<ID>_<Nombre>/          # Cuadernos (.ipynb), scripts (.py) o zips por estudiante
├── tarea_420908_inst_77381/         # Directorio con todas las entregas descargadas de T02
│   ├── submissions_summary.json     # Metadatos de alumnos y estado de entrega T02
│   └── User_<ID>_<Nombre>/          # Cuadernos (.ipynb) o zips por estudiante
├── reporte_calificaciones_T01_420907.csv  # Reporte detallado de T01 con desglose y feedback HTML
├── reporte_calificaciones_T02_420908.csv  # Reporte detallado de T02 con desglose y feedback HTML
└── reporte_consolidado_tareas.csv         # Reporte consolidado por alumno con promedio y notas
```

---

## 3. Rúbricas de Evaluación

### Rúbrica T01 (100 Puntos)
| Dimensión | Puntos | Criterio de Evaluación |
| :--- | :---: | :--- |
| **Preprocesamiento** | 25 | Mapeo binario de clase diagnóstica ($M \to 1, B \to 0$), exclusión del ID en $X$, partición $X/y$ y división 80/20 train/test. |
| **Escalamiento** | 20 | Uso de `StandardScaler` sin data leakage (`.fit_transform` en train, `.transform` en test). |
| **Modelado y Matrices** | 30 | Entrenamiento de k-NN ($n=5$), Árbol de Decisión ($depth=4$) y matrices de confusión para ambos. |
| **Fundamentación Teórica** | 25 | Explicación del riesgo clínico de un Falso Negativo (tumor maligno clasificado como benigno) y fundamentación matemática de por qué el árbol no se afecta por la escala. |

### Rúbrica T02 (100 Puntos)
| Dimensión | Puntos | Criterio de Evaluación |
| :--- | :---: | :--- |
| **Núcleo de Clase Base** | 40 | Carga del dataset Wine, partición estratificada, escalamiento y torneo multimodelo inicial (k-NN, Árbol, Bayes). |
| **Reto de Ampliación** | 25 | *Variante A:* Mapa de calor de correlación y selección justificada de la 3ra característica (Prolina, Fenoles, etc.).<br>*Variante B:* Integración de Regresión Logística / Pipeline y comparativa 4 modelos. |
| **Fronteras de Decisión** | 20 | Generación visual de fronteras de decisión espaciales (`DecisionBoundaryDisplay`). |
| **Análisis y Conclusiones** | 15 | Interpretación geométrica de las áreas de decisión y relevancia de escalar para k-NN. |

---

## 4. Casos Especiales Gestionados

1. **Archivos Intercambiados:**
   - `Cruz Trujillo Brayann Limberth` (UID: 189741) y `Casillas Carasani Brayan` (UID: 193316) subieron el archivo de T02 en T01, y el de T01 en T02. El sistema detectó automáticamente el cruce, evaluó el contenido en la tarea correspondiente y registró una nota explicativa en el feedback para el alumno sin perjudicar su puntaje (100/100 en ambas).
2. **Entrega Parcial (Solo tutorial de clase):**
   - `Condori Berdeja Juan Jose` (UID: 141808) entregó el cuaderno de clase en T02 sin agregar la sección del reto autónomo. Recibe 50/100 con retroalimentación explícita indicando qué parte faltó.
3. **Guías Anteriores Entregadas:**
   - `Mayta Baltazar Edemir` (UID: 199170) subió cuadernos correspondientes a guías anteriores (*Banknote Authentication* y *k-NN MinMaxScaler*). Se reconoce su esfuerzo con 80/100 en ambas entregas.
4. **Alumnos sin entrega:**
   - 4 estudiantes no registraron entrega en ninguna tarea y reciben 0/100.
   - `Aguilar Choque Clisman` entregó T01 (100) pero no T02 (0).
   - `Clemente Cruz Danitza` entregó T02 (95) pero no T01 (0).

---

## 5. Instrucciones de Uso

### Modo Simulación (Dry Run - No modifica eCampus):
```bash
python grade_assignments_int210.py
```

### Subida Directa a eCampus Moodle:
Para sincronizar las notas y retroalimentaciones HTML en la plataforma eCampus:
```bash
# Subir ambas tareas simultáneamente:
python grade_assignments_int210.py --push

# O subir de manera independiente:
python grade_assignments_int210.py --push-t01
python grade_assignments_int210.py --push-t02
```

