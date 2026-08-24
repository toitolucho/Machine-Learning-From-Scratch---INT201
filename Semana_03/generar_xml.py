import base64
import os

def get_b64(filename):
    with open(filename, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

b64_matriz = get_b64('matriz_confusion_phishing.png')
b64_frontera = get_b64('frontera_decision.png')

xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<quiz>
<!-- Categoria -->
  <question type="category">
    <category>
      <text>$course$/Semana 3: Modelos Supervisados</text>
    </category>
    <info format="html">
      <text><![CDATA[Cuestionario de la Semana 3 sobre k-NN y Regresión Logística.]]></text>
    </info>
  </question>

<!-- Pregunta 1: Drag and Drop sin grupos (Código k-NN) -->
  <question type="ddwtos">
    <name>
      <text>Q01. Completar instanciación k-NN</text>
    </name>
    <questiontext format="html">
      <text><![CDATA[<p>Complete el siguiente código para instanciar y entrenar un modelo k-Nearest Neighbors con 5 vecinos usando la métrica euclidiana:</p>
<pre>
from sklearn.neighbors import KNeighborsClassifier

modelo = [[1]]([[2]]=5, metric=[[3]])
modelo.[[4]](X_train, y_train)
</pre>]]></text>
    </questiontext>
    <defaultgrade>1.0000000</defaultgrade>
    <shuffleanswers>1</shuffleanswers>
    <dragbox><text>KNeighborsClassifier</text><group>1</group></dragbox>
    <dragbox><text>n_neighbors</text><group>1</group></dragbox>
    <dragbox><text>'euclidean'</text><group>1</group></dragbox>
    <dragbox><text>fit</text><group>1</group></dragbox>
    <dragbox><text>predict</text><group>1</group></dragbox>
    <dragbox><text>'manhattan'</text><group>1</group></dragbox>
  </question>

<!-- Pregunta 2: Drag and Drop sin grupos (Regresión Logística) -->
  <question type="ddwtos">
    <name>
      <text>Q02. Completar Regresión Logística</text>
    </name>
    <questiontext format="html">
      <text><![CDATA[<p>Complete el código para realizar predicciones con un modelo de Regresión Logística previamente entrenado y calcular la matriz de confusión:</p>
<pre>
from sklearn.metrics import confusion_matrix

y_pred = log_reg.[[1]](X_test)
matriz = [[2]]([[3]], [[4]])
</pre>]]></text>
    </questiontext>
    <defaultgrade>1.0000000</defaultgrade>
    <shuffleanswers>1</shuffleanswers>
    <dragbox><text>predict</text><group>1</group></dragbox>
    <dragbox><text>confusion_matrix</text><group>1</group></dragbox>
    <dragbox><text>y_test</text><group>1</group></dragbox>
    <dragbox><text>y_pred</text><group>1</group></dragbox>
    <dragbox><text>fit</text><group>1</group></dragbox>
    <dragbox><text>X_test</text><group>1</group></dragbox>
  </question>

<!-- Pregunta 3: Interpretación de Código/Imagen (Matriz) -->
  <question type="multichoice">
    <name>
      <text>Q03. Interpretación Matriz de Confusión</text>
    </name>
    <questiontext format="html">
      <text><![CDATA[<p>Observe la siguiente matriz de confusión generada por nuestro modelo detector de Phishing:</p>
<p><img src="data:image/png;base64,{b64_matriz}" alt="Matriz Confusión" width="450" /></p>
<p>Basado en la gráfica, ¿cuántos casos representan <strong>Falsos Negativos</strong> (sitios de Phishing reales que el modelo catalogó erróneamente como Legítimos)?</p>]]></text>
    </questiontext>
    <defaultgrade>1.0000000</defaultgrade>
    <penalty>0.3333333</penalty>
    <hidden>0</hidden>
    <single>true</single>
    <shuffleanswers>true</shuffleanswers>
    <answer fraction="100">
      <text><![CDATA[<p>10</p>]]></text>
      <feedback format="html"><text><![CDATA[<p>¡Correcto! En la esquina inferior izquierda se muestran los casos donde la etiqueta real era Phishing pero el modelo predijo Legítimo.</p>]]></text></feedback>
    </answer>
    <answer fraction="-33.33333">
      <text><![CDATA[<p>5</p>]]></text>
    </answer>
    <answer fraction="-33.33333">
      <text><![CDATA[<p>45</p>]]></text>
    </answer>
    <answer fraction="-33.33333">
      <text><![CDATA[<p>90</p>]]></text>
    </answer>
  </question>

<!-- Pregunta 4: Interpretación Frontera de Decisión -->
  <question type="multichoice">
    <name>
      <text>Q04. Frontera de Decisión</text>
    </name>
    <questiontext format="html">
      <text><![CDATA[<p>Analice la siguiente frontera de decisión obtenida al entrenar un modelo sobre 2 atributos:</p>
<p><img src="data:image/png;base64,{b64_frontera}" alt="Frontera de Decisión" width="450" /></p>
<p>¿Qué característica de la Regresión Logística se evidencia en esta gráfica?</p>]]></text>
    </questiontext>
    <defaultgrade>1.0000000</defaultgrade>
    <penalty>0.3333333</penalty>
    <hidden>0</hidden>
    <single>true</single>
    <shuffleanswers>true</shuffleanswers>
    <answer fraction="100">
      <text><![CDATA[<p>La frontera de separación entre ambas clases es estrictamente lineal en el espacio de características original.</p>]]></text>
    </answer>
    <answer fraction="-33.33333">
      <text><![CDATA[<p>El modelo se ha sobreajustado creando una frontera curva que rodea a los valores atípicos.</p>]]></text>
    </answer>
    <answer fraction="-33.33333">
      <text><![CDATA[<p>La gráfica demuestra que es un modelo no paramétrico basado en distancias locales.</p>]]></text>
    </answer>
    <answer fraction="-33.33333">
      <text><![CDATA[<p>El modelo es incapaz de clasificar los datos del centro.</p>]]></text>
    </answer>
  </question>

<!-- Pregunta 5: Selección Múltiple Teórica -->
  <question type="multichoice">
    <name><text>Q05. Fundamento de Regresión Logística</text></name>
    <questiontext format="html">
      <text><![CDATA[<p>¿Qué función matemática utiliza la Regresión Logística para aplastar la salida lineal al rango [0, 1] y estimar probabilidades?</p>]]></text>
    </questiontext>
    <defaultgrade>1</defaultgrade>
    <penalty>0.3333333</penalty>
    <single>true</single>
    <shuffleanswers>true</shuffleanswers>
    <answer fraction="100"><text><![CDATA[<p>La función Sigmoide</p>]]></text></answer>
    <answer fraction="-33.33333"><text><![CDATA[<p>La función ReLU</p>]]></text></answer>
    <answer fraction="-33.33333"><text><![CDATA[<p>La función Softmax plana</p>]]></text></answer>
    <answer fraction="-33.33333"><text><![CDATA[<p>La Transformada de Fourier</p>]]></text></answer>
  </question>

<!-- Pregunta 6: Verdadero / Falso -->
  <question type="truefalse">
    <name><text>Q06. k-NN y Normalización</text></name>
    <questiontext format="html">
      <text><![CDATA[<p>En el algoritmo k-Nearest Neighbors es fundamental normalizar o estandarizar los datos numéricos antes de entrenar, ya que el cálculo de distancias (como la Euclídea) es altamente sensible a las diferencias de magnitud entre las variables.</p>]]></text>
    </questiontext>
    <defaultgrade>1</defaultgrade>
    <answer fraction="100"><text>true</text></answer>
    <answer fraction="0"><text>false</text></answer>
  </question>

<!-- Pregunta 7: Verdadero / Falso -->
  <question type="truefalse">
    <name><text>Q07. Costo Operativo</text></name>
    <questiontext format="html">
      <text><![CDATA[<p>En un sistema de detección de Spam, un Verdadero Negativo ocurre cuando el modelo bloquea correctamente un correo basura.</p>]]></text>
    </questiontext>
    <defaultgrade>1</defaultgrade>
    <answer fraction="0"><text>true</text><feedback format="html"><text><![CDATA[<p>Falso. Un Verdadero Negativo es cuando un correo legítimo se clasifica correctamente como Legítimo.</p>]]></text></feedback></answer>
    <answer fraction="100"><text>false</text></answer>
  </question>

<!-- Pregunta 8: Respuesta Corta -->
  <question type="shortanswer">
    <name><text>Q08. Sintaxis Python</text></name>
    <questiontext format="html">
      <text><![CDATA[<p>En la librería scikit-learn, ¿cómo se llama el método utilizado para entrenar (ajustar) un modelo a los datos de entrenamiento? (Escriba solo el nombre del método, ej. en minúsculas)</p>]]></text>
    </questiontext>
    <defaultgrade>1</defaultgrade>
    <usecase>0</usecase>
    <answer fraction="100"><text>fit</text></answer>
    <answer fraction="100"><text>fit()</text></answer>
  </question>

<!-- Pregunta 9: Emparejamiento (Matching) -->
  <question type="matching">
    <name><text>Q09. Relacionar Conceptos de Matriz</text></name>
    <questiontext format="html"><text><![CDATA[<p>Relacione cada cuadrante de la matriz de confusión con su significado en ciberseguridad (Detección de Phishing, donde Positivo = Phishing):</p>]]></text></questiontext>
    <defaultgrade>1</defaultgrade>
    <shuffleanswers>true</shuffleanswers>
    <subquestion>
      <text><![CDATA[<p>Falso Positivo (FP)</p>]]></text>
      <answer><text>Sitio web legítimo bloqueado erróneamente por seguridad.</text></answer>
    </subquestion>
    <subquestion>
      <text><![CDATA[<p>Falso Negativo (FN)</p>]]></text>
      <answer><text>Sitio de Phishing que burló el sistema e ingresó como seguro.</text></answer>
    </subquestion>
    <subquestion>
      <text><![CDATA[<p>Verdadero Positivo (VP)</p>]]></text>
      <answer><text>Sitio de Phishing detectado y bloqueado exitosamente.</text></answer>
    </subquestion>
  </question>

<!-- Pregunta 10: Respuesta Corta -->
  <question type="shortanswer">
    <name><text>Q10. Librería Python</text></name>
    <questiontext format="html">
      <text><![CDATA[<p>Escriba el nombre de la librería principal en Python utilizada durante el laboratorio para leer archivos CSV y explorar DataFrames.</p>]]></text>
    </questiontext>
    <defaultgrade>1</defaultgrade>
    <usecase>0</usecase>
    <answer fraction="100"><text>pandas</text></answer>
  </question>

</quiz>
"""

with open('03_Cuestionario.xml', 'w', encoding='utf-8') as f:
    f.write(xml_content)
    
print("Archivo XML generado exitosamente.")
