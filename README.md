# Machine Learning From Scratch - INT201

Bienvenido al repositorio oficial del curso **INT210: Machine Learning From Scratch**, un programa de formación universitaria avanzada en Ciencia de Datos e Inteligencia Artificial enfocado en la construcción de algoritmos de aprendizaje automático desde sus cimientos matemáticos y computacionales puros, sin depender de librerías de caja negra.

---

## 🎯 Filosofía del Curso

El enfoque pedagógico combina tres pilares fundamentales:
1. **La Analogía de los 10 Años:** Comprensión intuitiva y visual de cada concepto abstracto antes de la formalización.
2. **Rigor Académico y Computacional:** Formalismo matemático, análisis de complejidad asintótica ($\mathcal{O}$) y optimización de memoria.
3. **Casos Reales Cruzados:** Aplicaciones prácticas en **Ciberseguridad** (análisis de tráfico, detección de intrusiones, filtrado de spam/phishing) y **Videojuegos / Arte Digital** (manipulación matricial RGB, geometría vectorial 3D, algoritmos de renderizado).

---

## 📚 Estructura Curricular del Repositorio

### 🔹 [Chapter 00: Nivelación Algorítmica y Estructuras de Datos](file:///d:/Documents/INT210/Machine%20Learning%20From%20Scratch%20-%20INT210/Chapter%2000)

#### 📌 [First Week: Fundamentos Algorítmicos y Control de Flujo](file:///d:/Documents/INT210/Machine%20Learning%20From%20Scratch%20-%20INT210/Chapter%2000/First%20Week)
* **[Sesión 0.1: Bifurcaciones Lógicas y Condicionales (`if`, `elif`, `else`)](file:///d:/Documents/INT210/Machine%20Learning%20From%20Scratch%20-%20INT210/Chapter%2000/First%20Week/Session_01_Condicionales_y_Bifurcaciones)**
  - Álgebra Booleana, tablas de verdad, *Truthiness*, cortocircuito lógico e identidad (`is` vs `==`).
  - *Casos:* Firewall por reglas y corrección de luminancia fotométrica ITU-R BT.601.
  - *Evaluación:* Clasificador heurístico de Spam y cálculo manual de la Matriz de Confusión (VP, VN, FP, FN).
* **[Sesión 0.2: Estructuras Multicamino y Diccionarios de Despacho](file:///d:/Documents/INT210/Machine%20Learning%20From%20Scratch%20-%20INT210/Chapter%2000/First%20Week/Session_02_MatchCase_y_Diccionarios_Despacho)**
  - `match-case` (Python 3.10+), *Dispatch Dictionaries* y complejidad temporal $\mathcal{O}(N)$ vs $\mathcal{O}(1)$.
  - *Casos:* Triaje automatizado de incidentes SOC y enrutador de renderizado multiformato (PNG, SVG, JPEG).
* **[Sesión 0.3: Bucles Deterministas (`for`), `enumerate` y Comprensiones](file:///d:/Documents/INT210/Machine%20Learning%20From%20Scratch%20-%20INT210/Chapter%2000/First%20Week/Session_03_Bucles_For_y_Comprensiones)**
  - Protocolo Iterador (`__iter__`, `__next__`), evaluación perezosa (*Lazy Evaluation*) vs RAM y *List Comprehensions*.
  - *Casos:* Transformación de matrices de píxeles RGB y auditoría forense de escaneo de puertos.
* **[Sesión 0.4: Bucles Indeterminados (`while`), Centinelas y Convergencia](file:///d:/Documents/INT210/Machine%20Learning%20From%20Scratch%20-%20INT210/Chapter%2000/First%20Week/Session_04_Bucles_While_y_Convergencia)**
  - Parada de Turing, condiciones centinela (`break`, `continue`) y criterio de convergencia numérica $\epsilon$.
  - *Casos:* *Network Listener* continuo y simulación de iluminación adaptativa iterativa.

#### 📌 [Second Week: Estructuras de Datos Nativas en Python](file:///d:/Documents/INT210/Machine%20Learning%20From%20Scratch%20-%20INT210/Chapter%2000/Second%20Week)
* **[Sesión 0.5: Listas, Tuplas y Vectores Matemáticos](file:///d:/Documents/INT210/Machine%20Learning%20From%20Scratch%20-%20INT210/Chapter%2000/Second%20Week/Session_05_Listas_Tuplas_y_Vectores)**
  - Álgebra Lineal *from scratch*, inmutabilidad, vectores $[x,y,z]$ y canales RGBA.
* **[Sesión 0.6: Diccionarios, `defaultdict` y Frecuencias](file:///d:/Documents/INT210/Machine%20Learning%20From%20Scratch%20-%20INT210/Chapter%2000/Second%20Week/Session_06_Diccionarios_Defaultdict_y_Frecuencias)**
  - Tablas hash $\mathcal{O}(1)$, mitigación de `KeyError` y análisis de frecuencia de palabras en Phishing (NLP).
* **[Sesión 0.7: Sets y Operaciones de Conjuntos en Alta Velocidad](file:///d:/Documents/INT210/Machine%20Learning%20From%20Scratch%20-%20INT210/Chapter%2000/Second%20Week/Session_07_Sets_y_Operaciones_de_Conjuntos)**
  - Álgebra de conjuntos ($A \cup B$, $A \cap B$, $A \setminus B$) y filtrado perimetral de IPs en Blacklists.
* **[Sesión 0.8: Ingesta de Archivos Delimitados "From Scratch"](file:///d:/Documents/INT210/Machine%20Learning%20From%20Scratch%20-%20INT210/Chapter%2000/Second%20Week/Session_08_Ingesta_Archivos_Nativos_From_Scratch)**
  - Parseo puro con `with open()` y `csv.reader` sin dependencias de Pandas.

---

## 🛠️ Estándar de Artefactos por Sesión

Cada sesión académica incluye 7 componentes esenciales:
1. `README.md`: Guía de estudio y objetivos claros para el alumno.
2. `0X_<Tema>.ipynb`: Cuaderno interactivo guiado con explicaciones paso a paso.
3. `0X_Guia_de_Trabajo_Soluciones.md`: Solucionario y notas metodológicas para el docente.
4. `0X_Laboratorio_Evaluacion.ipynb`: Reto práctico autónomo con bloques `# TODO`.
5. `0X_Soluciones_Laboratorio.md`: Respuestas y análisis de toma de decisiones de negocio.
6. `0X_Presentacion_Clase.tex`: Diapositivas académicas en LaTeX Beamer (*Tema Madrid / Color whale*).
7. `generar_graficas.py`: Script generador de gráficos visuales en alta resolución.
