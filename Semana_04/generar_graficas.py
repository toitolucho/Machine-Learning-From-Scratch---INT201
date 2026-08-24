import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def configurar_branding():
    color_fondo = '#F7FAFC'
    color_primario = '#1A365D'
    color_secundario = '#4A5568'
    color_acento = '#319795'
    
    plt.rcParams.update({
        'figure.facecolor': color_fondo,
        'axes.facecolor': color_fondo,
        'axes.edgecolor': color_secundario,
        'axes.labelcolor': color_secundario,
        'text.color': color_secundario,
        'xtick.color': color_secundario,
        'ytick.color': color_secundario,
        'font.family': 'sans-serif',
        'axes.titlesize': 14,
        'axes.titleweight': 'bold',
        'axes.titlecolor': color_primario,
        'lines.color': color_acento,
        'patch.edgecolor': color_fondo
    })

def plot_lasso_path():
    configurar_branding()
    
    alphas = np.logspace(-3, 1, 100)
    
    # Simular coeficientes encogiéndose a cero para Lasso
    coef_A = 1.0 * np.exp(-1.5 * alphas) # Importante, decae lento
    coef_B = 0.5 * np.exp(-4.0 * alphas) # Menos importante, decae rápido
    coef_C = 0.2 * np.exp(-8.0 * alphas) # Ruido, decae casi inmediato a cero
    
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(alphas, coef_A, label="Feature A (Crítica)", color='#1A365D', lw=3)
    ax.plot(alphas, coef_B, label="Feature B (Redundante)", color='#319795', lw=3)
    ax.plot(alphas, coef_C, label="Feature C (Ruido)", color='#4A5568', lw=2, linestyle='--')
    
    ax.set_xscale('log')
    ax.set_xlim(alphas[0], alphas[-1])
    ax.set_xlabel('Fuerza de Regularización (Alpha - Escala Log)')
    ax.set_ylabel('Valor del Coeficiente (w)')
    ax.set_title('El Inspector Lasso (L1) Vaciando la Mochila', pad=15)
    
    # Anotación pedagógica
    ax.annotate('Cae exactamente a Cero (Eliminada)', 
                xy=(0.02, 0.05), xytext=(0.05, 0.4),
                arrowprops=dict(facecolor='#4A5568', shrink=0.05),
                ha='left', color='#4A5568')
                
    ax.legend()
    plt.tight_layout()
    plt.savefig('d:/Documents/USFX/INT210/Machine-Learning-From-Scratch---INT210/Semana_04/lasso_path.png', dpi=300)
    plt.close()

if __name__ == "__main__":
    plot_lasso_path()
    print("lasso_path.png generated successfully.")
