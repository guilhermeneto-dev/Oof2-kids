import streamlit as st
import cv2
import numpy as np
from PIL import Image

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Missão Micro-Exploradores", layout="wide")

st.markdown("""
    <style>
    .main {background-color: #87CEEB;} /* Fundo Azul Céu */
    h1 {color: #FF4500; font-family: 'Comic Sans MS', cursive, sans-serif; text-shadow: 2px 2px #FFA500;}
    h3 {color: #00008B; font-family: 'Comic Sans MS', cursive, sans-serif;}
    .footer {position: fixed; left: 0; bottom: 0; width: 100%; background-color: #ffffff; color: #333; text-align: center; padding: 10px; font-size: 0.9em; border-top: 2px solid #FF4500; z-index: 999; font-family: sans-serif;}
    </style>
""", unsafe_allow_html=True)

st.title("🚀 Missão Micro-Exploradores!")
st.subheader("Encontre os Monstros do Vazio e Salve a Peça!")

# --- PAINEL DE CONTROLE (LATERAL) ---
st.sidebar.title("🎮 Painel da Nave")

st.sidebar.markdown("### 1. Escolha a sua Armadura")
armadura = st.sidebar.selectbox("De que material é feito nosso escudo?", 
                                ["Plástico de Impressora (Fraco)", "Ferro de Cavaleiro (Forte)", "Vibranium (Super Forte!)"])

if armadura == "Plástico de Impressora (Fraco)":
    forca_base = 100
elif armadura == "Ferro de Cavaleiro (Forte)":
    forca_base = 500
else:
    forca_base = 1000

st.sidebar.markdown("### 2. O Raio-X Mágico 🔍")
poder_raiox = st.sidebar.slider("Ajuste a força do Raio-X para achar os monstros:", 0, 255, 120)

st.sidebar.markdown("---")
st.sidebar.write("👨‍🚀 **Comandantes em Ação!**")

# --- ÁREA DO JOGO ---
uploaded_file = st.file_uploader("📸 Subam a foto da peça quebrada aqui!", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Lendo a foto
    image = Image.open(uploaded_file)
    img_array = np.array(image.convert('RGB'))
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    
    # A Mágica do Raio-X (Threshold disfarçado)
    _, binary = cv2.threshold(gray, poder_raiox, 255, cv2.THRESH_BINARY)
    
    # O Escudo de Energia (Malha OOF2 disfarçada)
    contours, _ = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    escudo_img = img_array.copy()
    cv2.drawContours(escudo_img, contours, -1, (0, 255, 0), 3)

    # Contando os Monstros (Matemática do Dano escondida)
    total_pixels = binary.size
    solid_pixels = cv2.countNonZero(binary)
    void_pixels = total_pixels - solid_pixels
    
    porcentagem_monstros = (void_pixels / total_pixels) * 100
    forca_atual = forca_base - (forca_base * (porcentagem_monstros / 100) * 1.5)
    if forca_atual < 0: forca_atual = 0

    # --- PLACAR DA MISSÃO ---
    st.write("### 🏆 Placar da Missão")
    col1, col2, col3 = st.columns(3)
    
    col1.metric("👾 Monstros Encontrados", f"{int(porcentagem_monstros)}%")
    col2.metric("🛡️ Força do Escudo", f"{int(forca_atual)} Pontos")
    col3.metric("🕸️ Teias de Energia", f"{len(contours)}")

    st.write("---")
    
    # --- TELAS DE VISUALIZAÇÃO ---
    t1, t2, t3 = st.columns(3)
    with t1:
        st.write("📸 **Foto Normal**")
        st.image(image, use_container_width=True)
    with t2:
        st.write("🔍 **Visão Raio-X**")
        st.image(binary, use_container_width=True)
    with t3:
        st.write("⚡ **Escudo de Energia!**")
        st.image(escudo_img, use_container_width=True)
        
    # RESULTADO DA MISSÃO
    if porcentagem_monstros > 20:
        st.error("🚨 ALERTA VERMELHO! Muitos monstros! A peça vai quebrar se a nave decolar! Precisamos imprimir de novo!")
    else:
        st.success("🌟 PARABÉNS! O escudo aguentou! A peça está segura e pronta para viajar no espaço!")
        st.balloons()
else:
    st.info("Aguardando a transmissão da foto da peça para começarmos a aventura...")

# --- RODAPÉ ---
st.markdown(
    """
    <div class="footer">
        <b>Comandante e Desenvolvedor:</b> Guilherme Fernandes Neto | <b>Base PPGEMec - UFSCar</b>
    </div>
    """,
    unsafe_allow_html=True
)
