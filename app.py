# Adaptado para Streamlit
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime

# Data atual
hoje_formatado = datetime.now().strftime("%d/%m/%Y")

# Competências
competencias = [
    "Design e Experiência do usuário","Voice of the Customer", "Fluência em dados",
    "Quality Assurance (QA)", "Product Delivery", "Especificação de features",
    "Managing Up", "Liderança de equipes", "Gerenciamento de stakeholders",
    "Impacto estratégico", "Visão de produto e construção de roadmap",
    "Ownership dos resultados de negócio", 
]

# Áreas e cores
cores_areas = {
    "Execução": "#FDECEA",
    "PrimeiroEspaco": "#FFFFFF",
    "Influenciando pessoas": "#F2E6F8",
    "SegundoEspaco": "#FFFFFF",
    "Estratégia de Produto":"#E6F4EC",
    "TerceiroEspaco": "#FFFFFF",
    "Insights sobre usuário":"#FFF9E5", 
    "QuartoEspaco": "#FFFFFF"
}

areas = {
    "Insights sobre usuário": [0, 1],
    "PrimeiroEspaco": [2],
    "Execução": [3, 4],
    "SegundoEspaco": [5],
    "Influenciando pessoas": [6, 7],
    "TerceiroEspaco": [8],
    "Estratégia de Produto": [9, 10],
    "QuartoEspaco": [11]
}

ponto_cores = ['#F1C40F']*3 + ['#E74C3C']*3 + ['#8E44AD']*3 + ['#1ABC9C']*3

# Título
st.title("📊 Radar de Competências para PMs")
st.write("Avalie de 0 a 10 cada uma das 12 competências listadas abaixo e gere seu gráfico de autoconhecimento.")

# Nome do usuário
nome_usuario = st.text_input("Seu nome")

# Inputs das competências
pontuacoes = []
for i, comp in enumerate(competencias):
    val = st.slider(comp, 0, 10, 5)
    pontuacoes.append(val)

# Botão
if st.button("Gerar Radar"):
    N = len(pontuacoes)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False) + np.pi / 12
    angles_looped = np.concatenate((angles, [angles[0]]))
    scores_scaled = [s / 2 for s in pontuacoes]
    scores_scaled_looped = scores_scaled + [scores_scaled[0]]
    escala_visual = 5

    fig, ax = plt.subplots(figsize=(7, 6))
    ax.set_aspect('equal')
    ax.set_xlim(-8.5, 8.5)
    ax.set_ylim(-7.5, 8.8)

    fig.text(0.02, 0.97, f"Radar de competências - {nome_usuario}", fontsize=11, ha='left', va='top', fontweight='bold')
    fig.text(0.98, 0.97, hoje_formatado, fontsize=9, ha='right', va='top', color='gray')

    for i in range(N):
        x = [0, escala_visual*np.cos(angles[i]), escala_visual*np.cos(angles[(i+1)%N])]
        y = [0, escala_visual*np.sin(angles[i]), escala_visual*np.sin(angles[(i+1)%N])]
        for nome_area, idxs in areas.items():
            if i in idxs:
                ax.fill(x, y, cores_areas[nome_area], alpha=1)
                break

    for r in range(1, escala_visual+1):
        x = r * np.cos(angles_looped)
        y = r * np.sin(angles_looped)
        ax.plot(x, y, color='lightgray', lw=0.8)

    ax.plot(escala_visual * np.cos(angles_looped), escala_visual * np.sin(angles_looped), color='black', linewidth=1.5)

    user_x = [r * np.cos(a) for r, a in zip(scores_scaled_looped, angles_looped)]
    user_y = [r * np.sin(a) for r, a in zip(scores_scaled_looped, angles_looped)]
    ax.fill(user_x, user_y, color="#9B59B6", alpha=0.15)
    ax.plot(user_x, user_y, color="#9B59B6", linewidth=1.2)

    for i in range(N):
        x = escala_visual * np.cos(angles[i])
        y = escala_visual * np.sin(angles[i])
        ax.plot(x, y, 'o', color=ponto_cores[i], markersize=4)
        nx = escala_visual * 0.88 * np.cos(angles[i])
        ny = escala_visual * 0.88 * np.sin(angles[i])
        ax.text(nx, ny, f"{pontuacoes[i]}", fontsize=8, ha='center', va='center', color='black', fontweight='bold')

    for i in range(N):
        x = (escala_visual + 0.6) * np.cos(angles[i])
        y = (escala_visual + 0.6) * np.sin(angles[i])
        ha = 'left' if np.cos(angles[i]) >= 0 else 'right'
        ax.text(x, y, competencias[i], fontsize=8, ha=ha, va='center')

    ax.plot([-8.8, 8], [0, 0], color='black', lw=1)
    ax.plot([0, 0], [-6, 6], color='black', lw=1)
    ax.plot([-6.5, 6.5], [-6.5, 6.5], color='lightgray', lw=0.7, ls='dashed')
    ax.plot([-6.5, 6.5], [6.5, -6.5], color='lightgray', lw=0.7, ls='dashed')

    ax.text(-7.9, 0.35, "Product Manager", fontsize=9, ha='right', va='bottom', fontweight='bold')
    ax.text(-7.9, -0.35, "Liderança de Produto", fontsize=9, ha='right', va='top', fontweight='bold')
    ax.text(-1.2, 6.2, "Construtor de produtos", fontsize=9, ha='right', va='bottom', fontweight='bold')
    ax.text(1.2, 6.2, "Arquiteto de produtos", fontsize=9, ha='left', va='bottom', fontweight='bold')

    ax.text(-2, 2.5, "Execução", fontsize=9, ha='center', va='center', color="#C0392B", fontweight='bold')
    ax.text(2, 2.5, "Insights sobre\nusuário", fontsize=9, ha='center', va='center', color="#D68910", fontweight='bold')
    ax.text(2.2, -2.2, "Estratégia\ndo produto", fontsize=9, ha='center', va='center', color="#1E8449", fontweight='bold')
    ax.text(-2.2, -2.2, "Influenciando\npessoas", fontsize=9, ha='center', va='center', color="#8E44AD", fontweight='bold')

    patches = [mpatches.Patch(color=cores_areas[k], label=k) for k in cores_areas if "Espaco" not in k]
    ax.legend(
        handles=patches,
        loc='lower left',
        fontsize=7,
        frameon=False,
        bbox_to_anchor=(-0.18, -0.14),
        borderaxespad=0
    )

    fig.text(0.98, 0.01, "Produzido por Gileard Teixeira\nwww.linkedin.com/in/gileard-teixeira",
             fontsize=8, ha='right', va='bottom', color='gray', fontstyle='italic')

    ax.axis('off')
    plt.tight_layout()
    st.pyplot(fig)
