import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
import base64
import os

# Configuración estricta del branding académico
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Inter', 'Montserrat', 'Arial']
sns.set_palette(['#319795', '#1A365D', '#4A5568'])
COLOR_PRIMARIO = '#1A365D'
COLOR_ACENTO = '#319795'
COLOR_NEUTRAL = '#4A5568'
BG_COLOR = '#F7FAFC'

def image_to_base64(filepath):
    with open(filepath, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

def generar_matriz_confusion_phishing():
    # Simulamos una matriz de confusión para un detector de Phishing
    # 0 = Phishing (Positivo en nuestro contexto de detección), 1 = Legítimo (Negativo)
    y_true = [0]*45 + [0]*10 + [1]*5 + [1]*90
    y_pred = [0]*45 + [1]*10 + [0]*5 + [1]*90
    
    cm = confusion_matrix(y_true, y_pred)
    
    fig, ax = plt.subplots(figsize=(6, 5))
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Phishing', 'Legítimo'])
    disp.plot(cmap=sns.light_palette(COLOR_ACENTO, as_cmap=True), ax=ax, text_kw={'color': COLOR_PRIMARIO, 'fontsize': 14, 'weight': 'bold'})
    
    ax.set_title('Matriz de Confusión: Modelo k-NN', color=COLOR_PRIMARIO, fontsize=16, pad=15)
    ax.set_xlabel('Predicción del Modelo', color=COLOR_NEUTRAL, fontsize=12)
    ax.set_ylabel('Realidad (Etiqueta Verdadera)', color=COLOR_NEUTRAL, fontsize=12)
    
    plt.tight_layout()
    filepath = 'matriz_confusion_phishing.png'
    plt.savefig(filepath, dpi=150, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    return filepath

def generar_frontera_decision():
    # Frontera de decisión simple de regresión logística
    X, y = make_classification(n_samples=100, n_features=2, n_redundant=0, n_informative=2,
                               random_state=42, n_clusters_per_class=1, flip_y=0.1)
    
    clf = LogisticRegression()
    clf.fit(X, y)
    
    fig, ax = plt.subplots(figsize=(7, 5))
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    
    # Meshgrid
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.02),
                         np.arange(y_min, y_max, 0.02))
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    
    # Plot contour and scatter
    ax.contourf(xx, yy, Z, alpha=0.3, cmap=sns.color_palette("blend:"+COLOR_NEUTRAL+","+COLOR_ACENTO, as_cmap=True))
    scatter = ax.scatter(X[:, 0], X[:, 1], c=y, edgecolors='k', cmap=sns.color_palette("blend:"+COLOR_NEUTRAL+","+COLOR_ACENTO, as_cmap=True))
    
    ax.set_title('Frontera de Decisión Logística (Sigmoide)', color=COLOR_PRIMARIO, fontsize=14, pad=15)
    ax.set_xlabel('Atributo X1', color=COLOR_NEUTRAL)
    ax.set_ylabel('Atributo X2', color=COLOR_NEUTRAL)
    
    plt.tight_layout()
    filepath = 'frontera_decision.png'
    plt.savefig(filepath, dpi=150, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    return filepath

if __name__ == '__main__':
    fp_matriz = generar_matriz_confusion_phishing()
    fp_frontera = generar_frontera_decision()
    
    b64_matriz = image_to_base64(fp_matriz)
    b64_frontera = image_to_base64(fp_frontera)
    
    print("\n--- INICIO BASE64 MATRIZ ---")
    print(b64_matriz)
    print("--- FIN BASE64 MATRIZ ---\n")
    
    print("\n--- INICIO BASE64 FRONTERA ---")
    print(b64_frontera)
    print("--- FIN BASE64 FRONTERA ---\n")
