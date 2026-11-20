# Proyecto P01: Detección de inicios de sesión sospechosos en el Sistema Académico

**Asignatura:** INT201 – Machine Learning
**Evaluación:** Segundo Parcial – Gestión 02-2026
**Modalidad:** {{individual / en parejas}}
**Fecha de entrega:** {{fecha}} · **Defensa oral:** {{fecha}}

---

## 1. Objetivos

**Objetivo general.** Desarrollar un modelo de clasificación que identifique, en el momento del inicio de
sesión, los intentos de acceso sospechosos al Sistema Integrado Académico, justificando cada decisión con
evidencia.

**Objetivos específicos.** Al concluir el proyecto, el estudiante deberá ser capaz de:

1. Interpretar el contexto del caso e identificar las restricciones que condicionan la solución.
2. Explorar el registro de inicios de sesión y detectar problemas de calidad en los datos.
3. Decidir y justificar qué registros y columnas se conservan, corrigen, transforman o excluyen.
4. Entrenar y comparar al menos dos modelos de clasificación vistos en la asignatura.
5. Seleccionar la métrica de evaluación adecuada al caso y justificar el modelo recomendado.
6. Contrastar las hipótesis planteadas por la Dirección de TI con evidencia.
7. Comunicar los resultados en un lenguaje comprensible para la Dirección de TI.

## 2. Descripción del caso

La Dirección de Tecnologías de la Información (DTI) de la universidad administra el Sistema Integrado Académico
(SIA), plataforma en la que estudiantes, docentes y personal administrativo consultan notas, realizan
inscripciones y registran pagos.

Durante septiembre se detectaron accesos no autorizados a varias cuentas: se modificaron correos de
recuperación y, en un caso, se intentó alterar una calificación. El Centro de Operaciones de Seguridad (SOC)
revisó dos meses de registros de inicio de sesión e identificó los intentos que correspondían a ataques
confirmados.

La DTI requiere un mecanismo que, en el momento en que un usuario presiona «Ingresar», determine si el intento
es normal o sospechoso. Ante un intento sospechoso, el SIA solicitará un código de verificación adicional (2FA)
antes de permitir el acceso.

## 3. Pregunta de negocio y variable objetivo

- **Pregunta de negocio:** ¿Es posible identificar, en el instante del inicio de sesión, los intentos que
  probablemente corresponden a un ataque?
- **Variable objetivo:** `es_ataque` — 1 si el SOC confirmó el intento como ataque; 0 en caso contrario.

## 4. Restricciones y condiciones del caso

- **Momento de la predicción:** la decisión se toma cuando el usuario presiona «Ingresar», antes de que la
  sesión comience y antes de que cualquier persona revise el caso.
- **Costo de los errores:**
  - Un ataque no detectado permite al atacante modificar datos, acceder a información personal o alterar
    calificaciones.
  - Un usuario legítimo clasificado como sospechoso solo debe ingresar un código 2FA (aproximadamente 30
    segundos).
  - La DTI prefiere solicitar 2FA en exceso antes que permitir un ataque; sin embargo, si más de la mitad de las
    alertas resultan falsas, los usuarios rechazarán el mecanismo.
- **Usuarios del resultado:** el propio SIA, de forma automática, y los analistas del SOC, que necesitan
  comprender por qué un intento fue clasificado como sospechoso.
- **Particularidades de los datos:**
  - El equipo de Control de Calidad (QA) ejecuta pruebas automáticas cada madrugada con las cuentas
    `qa_bot_01` a `qa_bot_05`, desde la red interna `10.0.99.x`. Estas pruebas simulan, de forma intencional,
    numerosos intentos rápidos.
  - Cuando el servidor de registros se reinicia, reenvía algunos registros que ya había enviado.
  - El servicio de geolocalización no siempre logra determinar el país de origen, por ejemplo cuando la conexión
    pasa por una VPN o por la red Tor.

## 5. Descripción de los datos

| Archivo | Registros | Descripción |
|---|---|---|
| `data/logins_sia.csv` | 4 270 | Un registro por intento de inicio de sesión, del 1 de septiembre al 30 de octubre de 2026 |

**Diccionario de datos** (según la información proporcionada por la DTI):

| Columna | Descripción |
|---|---|
| `evento_id` | Código del evento en el registro del sistema. |
| `fecha_hora` | Fecha y hora del intento de inicio de sesión. |
| `usuario` | Código de la cuenta (estudiantes `u…`, docentes `doc.…`, administrativos `adm.…`). |
| `rol` | Tipo de cuenta: estudiante, docente o administrativo. |
| `ip_origen` | Dirección IP desde la que se realizó el intento. |
| `pais_geo` | País estimado a partir de la IP. Lo registran distintos servicios, por lo que su formato no es uniforme. |
| `navegador` | Navegador o programa que realizó la solicitud. Lo informa el propio cliente; su formato varía. |
| `sistema_operativo` | Sistema operativo informado por el cliente. |
| `intentos_fallidos_previos_1h` | Intentos fallidos de la cuenta en la hora anterior, calculados por el SIA en el momento del inicio de sesión. El contador presentó errores en algunos registros. |
| `segundos_desde_intento_anterior` | Segundos transcurridos desde el intento anterior de la misma cuenta. Se calcula con relojes de varios servidores. |
| `dispositivo_nuevo` | 1 si el SIA no reconoce el dispositivo para esa cuenta. |
| `usa_vpn` | 1 si la IP pertenece a un proveedor conocido de VPN. |
| `duracion_sesion_min` | Minutos que duró la sesión. Se registra cuando el usuario cierra la sesión o esta expira. |
| `version_app` | Versión del SIA en la que ocurrió el evento. |
| `tema_interfaz` | Tema visual configurado por el usuario (claro u oscuro). |
| `bloqueado_por_soporte` | 1 si la Mesa de Ayuda bloqueó la cuenta después de revisar el caso. Se actualiza al cerrar el ticket, normalmente entre 1 y 3 días después. |
| `es_ataque` | Variable objetivo: 1 si el SOC confirmó el intento como ataque. |

## 6. Hipótesis planteadas por el cliente

La DTI plantea las siguientes hipótesis, que el estudiante deberá **confirmar o refutar** con evidencia
(conteos, tablas, gráficos o métricas):

- **H1.** La mayoría de los ataques ocurre de madrugada.
- **H2.** Las cuentas docentes son las más atacadas, porque permiten modificar calificaciones.
- **H3.** El uso de la columna `bloqueado_por_soporte` permitirá obtener un detector prácticamente perfecto.
- **H4.** Los registros sin país son defectuosos y pueden eliminarse sin perder información relevante.

## 7. Actividades a desarrollar

El proyecto no sigue una secuencia de pasos predefinida. El estudiante deberá decidir qué tratamiento aplicar a
los datos y justificar cada decisión en la bitácora. Las preguntas orientadoras de cada fase sirven como guía.

### Fase 1. Comprensión de los datos
El estudiante deberá describir la estructura del conjunto de datos y su calidad.
- ¿Qué representa cada registro? ¿Cuántos registros hay de cada clase?
- ¿Existen valores faltantes, repetidos, imposibles o escritos de formas distintas?
- ¿Todos los registros corresponden a intentos reales de usuarios del SIA?

### Fase 2. Preparación de los datos
El estudiante deberá definir y aplicar el tratamiento de los datos.
- ¿Qué columnas aportan información útil, cuáles no aportan y cuáles no deberían usarse según el momento de la
  predicción (sección 4)?
- ¿Qué registros deben excluirse o corregirse, y qué efecto tendría conservarlos?
- ¿Existe información contenida en alguna columna que pueda transformarse en una variable más útil?
- ¿Qué transformaciones requieren las variables para ser utilizadas por los modelos (codificación, escalado,
  tratamiento de faltantes)?

### Fase 3. Modelado
El estudiante deberá entrenar y comparar al menos dos modelos vistos en la asignatura (regresión logística,
k-NN, árbol de decisión, Naive Bayes, Random Forest).
- ¿Cómo se dividieron los datos y por qué la evaluación es válida, considerando la proporción de ataques?

### Fase 4. Evaluación
El estudiante deberá seleccionar la métrica principal según las condiciones del caso y justificar el modelo
recomendado.
- ¿Qué métrica refleja mejor el costo de los errores descrito en la sección 4?
- ¿Qué modelo, configuración y umbral de decisión se recomiendan?
- ¿Cada hipótesis de la DTI se cumple o no se cumple? ¿Con qué evidencia?

### Fase 5. Conclusiones y recomendación
El estudiante deberá presentar la solución en lenguaje de la DTI.
- ¿Qué hace la solución, qué tan bien funciona y qué limitaciones tiene?
- ¿Qué datos adicionales permitirían mejorar el detector?

## 8. Requisitos mínimos

1. El notebook debe ejecutarse completo, de principio a fin, sin errores.
2. Cada decisión sobre los datos debe estar registrada en la bitácora con su evidencia.
3. Se deben comparar al menos dos modelos con la misma división de datos.
4. La métrica principal debe justificarse con las condiciones del caso.
5. Las cuatro hipótesis deben responderse.

## 9. Entregables

| N.º | Entregable | Formato |
|---|---|---|
| 1 | Notebook con el desarrollo completo | `.ipynb` |
| 2 | Bitácora de decisiones (`bitacora_decisiones.md`, adjunta) | `.md` |
| 3 | Resumen ejecutivo dirigido a la DTI (máximo una página, sin código) | `.pdf` o `.md` |

## 10. Defensa oral

La defensa tiene una duración de 10 minutos y se desarrolla en tres partes:

1. **Presentación** (3 min): el estudiante expone la solución como si se dirigiera a la DTI.
2. **Preguntas** (4 min): el docente consulta sobre las decisiones registradas en la bitácora y los resultados
   obtenidos.
3. **Tarea en el notebook** (3 min): el docente solicita una modificación o un análisis adicional en el
   notebook; el estudiante deberá realizarlo y explicar el resultado.

El estudiante deberá contar con su notebook abierto y ejecutable durante la defensa.

## 11. Criterios de evaluación

| Criterio | Ponderación |
|---|---|
| Comprensión del caso y de sus restricciones | 15 % |
| Preparación de datos justificada en la bitácora | 25 % |
| Modelado y evaluación (división válida, comparación, métrica pertinente) | 20 % |
| Contraste de hipótesis con evidencia | 10 % |
| Resumen ejecutivo para la DTI | 10 % |
| Defensa oral (explicación, respuestas y tarea en el notebook) | 20 % |

La calificación del trabajo escrito se ajusta según la defensa: las decisiones que el estudiante no pueda
explicar no se consideran parte de su trabajo.
