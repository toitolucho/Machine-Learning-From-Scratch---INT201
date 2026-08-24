<div style="font-family: 'Inter', sans-serif; color: #4A5568;">

<h1 style="color: #1A365D; font-family: 'Montserrat', sans-serif;">Semana 3: Modelos Supervisados de Clasificación Clásica (k-NN y Regresión Logística)</h1>

<p>Bienvenidos a la tercera semana. Esta semana nos adentraremos en dos de los algoritmos clásicos fundamentales del Machine Learning. Evaluaremos estos modelos en contextos reales de ciberseguridad, como la detección de sitios web de Phishing y la clasificación de correos Spam, enfatizando el impacto en el negocio que tienen los errores de clasificación.</p>

<h2 style="color: #319795; font-family: 'Montserrat', sans-serif;">Objetivo de la Semana</h2>
<p>Comprender y aplicar el algoritmo <strong>k-Nearest Neighbors (k-NN)</strong> y la <strong>Regresión Logística</strong>. Aprenderás a sintonizar hiperparámetros (como <em>k</em> y la regularización <em>C</em>) y a interpretar la <strong>Matriz de Confusión</strong> para decidir, desde una perspectiva de negocio, el costo de bloquear un acceso legítimo (Falso Positivo) frente a dejar pasar una amenaza real (Falso Negativo).</p>

<h2 style="color: #319795; font-family: 'Montserrat', sans-serif;">Contenido</h2>

<ol>
    <li><strong style="color: #1A365D;"><code>03_Clasificacion_Supervisada.ipynb</code></strong>: Cuaderno guiado donde entrenaremos un modelo detector de Phishing, explorando la intuición detrás del tobogán logístico y los vecinos más cercanos.</li>
    <li><strong style="color: #1A365D;"><code>03_Laboratorio_Evaluacion.ipynb</code></strong>: Reto autónomo. Asumirás el rol de Director de Ciberseguridad analizando un dataset de SPAM y defenderás matemáticamente tu elección de modelo para producción.</li>
    <li><strong style="color: #1A365D;"><code>03_Tarea.ipynb</code></strong>: Reto guiado para graficar las fronteras de decisión y las curvas de aprendizaje, identificando exactamente dónde el modelo sufre sobreajuste (Overfitting).</li>
    <li><strong style="color: #1A365D;">Presentaciones</strong>: Explicación teórica exhaustiva de las métricas de distancia, la función sigmoide y el análisis de negocio de la Matriz de Confusión.</li>
</ol>

<h2 style="color: #319795; font-family: 'Montserrat', sans-serif;">Requisitos</h2>
<ul>
    <li>Las librerías base de esta semana incluyen funciones de <code style="font-family: 'JetBrains Mono', monospace; background-color: #F7FAFC;">sklearn.neighbors</code> como <code style="font-family: 'JetBrains Mono', monospace; background-color: #F7FAFC;">KNeighborsClassifier</code>, y <code style="font-family: 'JetBrains Mono', monospace; background-color: #F7FAFC;">sklearn.linear_model</code> como <code style="font-family: 'JetBrains Mono', monospace; background-color: #F7FAFC;">LogisticRegression</code>, además de métricas de <code style="font-family: 'JetBrains Mono', monospace; background-color: #F7FAFC;">sklearn.metrics</code>.</li>
</ul>

</div>
