# Guía de Calificación y Ajuste: Preguntas Drag & Drop (ddwtos) con 2 Categorías
## Primer Parcial 02-2026 | Machine Learning INT210

---

## 1. Causa Raíz del Problema Técnico en Moodle

En el tipo de pregunta **Arrastrar y Soltar sobre Texto (`ddwtos`)**, Moodle implementa una vinculación posicional estricta:
1. El marcador `[[1]]` en el enunciado se vincula **única y exclusivamente** al elemento `<dragbox>` número 1 declarado en el XML.
2. El marcador `[[2]]` se vincula **única y exclusivamente** al elemento `<dragbox>` número 2 declarado en el XML.
3. **Herencia de Grupo**: El hueco `[[N]]` solo admite fichas que pertenezcan al mismo `<group>` que la opción `N`.

### ¿Por qué falló el segundo hueco?
Al generarse las preguntas, las opciones se ordenaron agrupando primero todas las fichas de la categoría 1 y luego las de la categoría 2:
- **Opción 1**: Respuesta correcta de `[[1]]` (`<group>1</group>`) $\rightarrow$ **Válida**.
- **Opción 2**: Distractor de la categoría 1 (`<group>1</group>`). Al ser la segunda opción en el XML, Moodle la asoció automáticamente al hueco `[[2]]` y fijó el hueco `[[2]]` como receptor exclusivo del **Grupo 1**.
- **Opción 3/4**: Respuesta correcta de `[[2]]` (`<group>2</group>`). Al pertenecer al Grupo 2 y estar el hueco `[[2]]` fijado al Grupo 1, **Moodle impidió físicamente soltarla en la pantalla** (rebota y no encaja).

### Consecuencia
- El hueco **`[[1]]` funcionó al 100%**: los estudiantes pudieron arrastrar y soltar la respuesta correcta sin inconvenientes.
- El hueco **`[[2]]` quedó completamente inhabilitado** para la opción correcta.

---

## 2. Criterio de Calificación Justa (Ajuste a Solo el Primer Hueco)

Para garantizar equidad pedagógica y no perjudicar a los estudiantes por la limitación técnica:
1. **Anulación del Hueco 2**: Se desestima por completo el resultado del hueco `[[2]]`.
2. **Calificación basada al 100% en el Hueco 1**:
   - Si el estudiante colocó correctamente la ficha del **Hueco `[[1]]`**, se le asigna la **puntuación total de la pregunta (1.00 / 1.00)**.
   - Si el estudiante falló o dejó vacío el **Hueco `[[1]]`**, se le asigna **0.00 / 1.00**.
3. **Puntuación Moodle por defecto vs. Ajuste**:
   - Moodle asignó automáticamente `0.50 / 1.00` a quienes respondieron bien `[[1]]` (o `0.25` en Q07 y `0.67` en Q14).
   - El ajuste consiste en sumar la fracción faltante (+0.50 pts por defecto) para que alcancen el 1.00 completo.

---

## 3. Lista de Preguntas Afectadas: Parte 2 - Pandas
**Archivo evaluado:** `Quiz_Parte2_Pandas.xml`  
**Total preguntas ddwtos con 2 categorías:** 9 preguntas

| N° | Nombre de la Pregunta | Snippet de Código | Hueco [[1]] (Calificable - 100%) | Hueco [[2]] (Inhabilitado - Condonado) | Puntaje Original Moodle si [[1]] es OK | Puntaje Ajustado |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: |
| **Q01** | Carga de archivo CSV con Pandas | `import pandas as [[1]]`<br>`df = pd.[[2]]("characters_clean.csv")` | `pd` *(Group 1)* | `read_csv` *(Group 2)* | 0.50 / 1.00 | **1.00** |
| **Q04** | Estadisticas descriptivas y percentiles | `estadisticas = df.[[1]]().[[2]](2)` | `describe` *(Group 1)* | `round` *(Group 2)* | 0.50 / 1.00 | **1.00** |
| **Q06** | Generacion de histogramas y diagramas de caja | `df["production_hours"].plot(kind=[[1]])`<br>`df.plot(kind=[[2]], y="production_hours")` | `hist` *(Group 1)* | `"box"` *(Group 2)* | 0.50 / 1.00 | **1.00** |
| **Q11** | Agregacion por grupos con groupby | `promedio_estilo = df.[[1]]("style")[[[2]]].mean()` | `groupby` *(Group 1)* | `"production_hours"` *(Group 2)* | 0.50 / 1.00 | **1.00** |
| **Q13** | Seleccion de columnas numericas y matriz de correlacion | `df_num = df.[[1]](include="number")`<br>`matriz_corr = df_num.[[2]]()` | `select_dtypes` *(Group 1)* | `corr` *(Group 2)* | 0.50 / 1.00 | **1.00** |
| **Q17** | Codificacion One-Hot con get_dummies | `df_encoded = pd.[[1]](df, columns=["role"], [[2]]=True)` | `get_dummies` *(Group 1)* | `drop_first` *(Group 2)* | 0.50 / 1.00 | **1.00** |
| **Q20** | Mapeo ordinal para variable jerarquica style | `df["style_code"] = df["style"].[[1]]([[2]])` | `map` *(Group 1)* | `style_map` *(Group 2)* | 0.50 / 1.00 | **1.00** |
| **Q22** | Filtrado por umbral de correlacion | `[col for col in corr_target.index if [[1]](corr_target[col]) >= [[2]]]` | `abs` *(Group 1)* | `umbral` *(Group 2)* | 0.50 / 1.00 | **1.00** |
| **Q24** | Exportacion a disco sin indice | `df_features.[[1]]("characters_features.csv", [[2]]=False)` | `to_csv` *(Group 1)* | `index` *(Group 2)* | 0.50 / 1.00 | **1.00** |

*(Nota: La pregunta **Q09** utiliza únicamente el Grupo 1 y no tuvo este conflicto).*

---

## 4. Lista de Preguntas Afectadas: Parte 3 - Regresión Lineal
**Archivo evaluado:** `Quiz_Parte3_RegresionLineal.xml`  
**Total preguntas ddwtos con 2 categorías:** 6 preguntas

| N° | Nombre de la Pregunta | Snippet de Código | Hueco [[1]] (Calificable - 100%) | Hueco [[2]] (Inhabilitado - Condonado) | Puntaje Original Moodle si [[1]] es OK | Puntaje Ajustado |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: |
| **Q05** | Ensamblaje de matriz con termino de bias | `ones = np.[[1]]((len(y), 1))`<br>`X_b = np.[[2]]([ones, X])` | `ones` *(Group 1)* | `hstack` *(Group 2)* | 0.50 / 1.00 | **1.00** |
| **Q07** | Implementacion de la Ecuacion Normal con NumPy | `beta_simple = np.linalg.[[1]](X_simple.T [[2]] X_simple) [[2]] X_simple.T [[2]] y` | `inv` *(Group 1)* | `@` *(Group 2 - 3 huecos)* | 0.25 / 1.00 | **1.00** |
| **Q11** | Calculo de residuos y Error Absoluto Medio | `residuos = y - y_pred`<br>`mae = np.[[1]](np.[[2]](residuos))` | `mean` *(Group 1)* | `abs` *(Group 2)* | 0.50 / 1.00 | **1.00** |
| **Q14** | Division de datos con train_test_split | `from sklearn.model_selection import [[1]]`<br>`X_tr, X_te, y_tr, y_te = [[1]](X, y, test_size=[[2]])` | `train_test_split` *(Group 1 - 2 huecos)* | `0.20` *(Group 2)* | 0.67 / 1.00 | **1.00** |
| **Q16** | Ajuste y prediccion en LinearRegression | `model.[[1]](X_train, y_train)`<br>`y_pred_test = model.[[2]](X_test)` | `fit` *(Group 1)* | `predict` *(Group 2)* | 0.50 / 1.00 | **1.00** |
| **Q22** | Grafico diagnostico de residuos y linea horizontal | `plt.scatter(y_pred, residuos)`<br>`plt.[[1]](y=[[2]], linestyle="--")` | `axhline` *(Group 1)* | `0` *(Group 2)* | 0.50 / 1.00 | **1.00** |

---

## 5. Instrucciones para Recalificar en Moodle

### Opción 1: Recalificación Manual en Moodle (Recomendada para pocos estudiantes)
1. Ingrese al Cuestionario en Moodle.
2. Vaya a **Resultados** $\rightarrow$ **Calificación manual** (o haga clic en los intentos de los estudiantes).
3. Ubique las preguntas listadas en las tablas anteriores.
4. Para cada estudiante que tenga el primer hueco correcto (marcado con ticket verde en `[[1]]` y puntaje parcial `0.50`, `0.25` o `0.67`):
   - Ingrese `1.00` en la casilla de calificación manual de la pregunta.
   - En el comentario opcional puede indicar: *"Ajuste técnico por condonación de categoría 2"*.
5. Guarde los cambios.

### Opción 2: Script en Python para Ajuste Automatizado vía CSV de Moodle
Si se descargan las calificaciones detalladas desde **Resultados $\rightarrow$ Respuestas detalladas (CSV)**, se puede ejecutar el siguiente script para recalcular la nota final automáticamente:

```python
import pandas as pd

# 1. Cargar el reporte exportado de Moodle
df_calif = pd.read_csv("reporte_moodle.csv")

# 2. Columnas correspondientes a las preguntas afectadas
preguntas_ajustables = [
    # Pandas
    "P. 1 /1.00", "P. 4 /1.00", "P. 6 /1.00", "P. 11 /1.00", 
    "P. 13 /1.00", "P. 17 /1.00", "P. 20 /1.00", "P. 22 /1.00", "P. 24 /1.00",
    # Regresion Lineal (ajustar segun el numero de columna en el quiz correspondiente)
    "P. 5 /1.00", "P. 7 /1.00", "P. 11 /1.00", "P. 14 /1.00", "P. 16 /1.00", "P. 22 /1.00"
]

for col in preguntas_ajustables:
    if col in df_calif.columns:
        # Si el estudiante obtuvo puntaje parcial mayor a 0 (acerto el hueco 1), otorgar 1.00
        df_calif[col] = df_calif[col].apply(lambda score: 1.00 if score > 0 else 0.00)

# Recalcular calificacion final
# Guardar archivo con notas corregidas
df_calif.to_csv("reporte_moodle_recalificado.csv", index=False)
print("Recalificacion completada con exito.")
```

---

## 6. Archivos XML Corregidos Disponibles

Para futuras evaluaciones o reinicios de cuestionario, se han generado y validado las versiones corregidas con el orden estricto de opciones:
- `Quiz_Parte2_Pandas_Corregido.xml`
- `Quiz_Parte3_RegresionLineal_Corregido.xml`

En estas versiones, Choice 1 corresponde exactamente a `[[1]]` (Grupo 1), Choice 2 a `[[2]]` (Grupo 2), y todos los distractores se ubican del Choice 3 en adelante, permitiendo el arrastre fluido y la calificación nativa sin errores.
