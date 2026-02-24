import streamlit as st

st.set_page_config(page_title="El bebé de Camilo & Angelica", layout="centered")

# --- ESTILO CSS GLOBAL ---
st.markdown("""
    <style>
    .main {
        background-color: #fdfaf5;
    }
    /* Estilo para los botones normales (fuera del grid) */
    .stButton>button {
        border-radius: 20px;
        transition: all 0.3s;
    }
    /* Aviso para celulares */
    @media only screen and (max-width: 600px) {
        .mobile-warn {
            background-color: #fff3cd; color: #856404; padding: 10px;
            border-radius: 5px; text-align: center; margin-bottom: 15px; font-weight: bold;
        }
    }
    @media only screen and (min-width: 601px) {
        .mobile-warn { display: none; }
    }
    </style>
    """, unsafe_allow_html=True)


# --- FUNCIÓN PARA LOS BORDES DEL GRID (#) ---
def obtener_bordes(i, j):
    """Aplica tu lógica para dejar solo las líneas internas del Triki."""
    css = ""
    css += "border-top: 4px solid #2c3e50 !important; " if i > 0 else "border-top: none !important; "
    css += "border-bottom: 4px solid #2c3e50 !important; " if i < 2 else "border-bottom: none !important; "
    css += "border-left: 4px solid #2c3e50 !important; " if j > 0 else "border-left: none !important; "
    css += "border-right: 4px solid #2c3e50 !important; " if j < 2 else "border-right: none !important; "
    return css


# --- ESTADO DE LA SESIÓN ---
if "tablero" not in st.session_state:
    st.session_state.tablero = [["" for _ in range(3)] for _ in range(3)]
    st.session_state.turno = None
    st.session_state.jugador1 = None
    st.session_state.ganador = None
    st.session_state.modo_revelacion = False
    st.session_state.revelados = [[False for _ in range(3)] for _ in range(3)]

revelacion_map = {
    (0, 0): "Niño", (1, 1): "Niño", (2, 0): "Niño", (2, 1): "Niño",
    (0, 2): "Niña", (1, 2): "Niña", (1, 0): "Niña", (0, 1): "Niña",
    (2, 2): "Dinos cuál es"
}


def verificar_ganador(tablero):
    for i in range(3):
        if tablero[i][0] == tablero[i][1] == tablero[i][2] != "": return True
        if tablero[0][i] == tablero[1][i] == tablero[2][i] != "": return True
    if tablero[0][0] == tablero[1][1] == tablero[2][2] != "": return True
    if tablero[0][2] == tablero[1][1] == tablero[2][0] != "": return True
    return False


st.markdown(
    '<div class="mobile-warn">📱 Para una mejor experiencia, gira tu celular de forma horizontal (Landscape) 🔄</div>',
    unsafe_allow_html=True)

# --- DENTRO DE LA VISTA 1: MODO REVELACIÓN ---
if st.session_state.modo_revelacion:
    st.title("🕵️‍♂️ Revelación de Posiciones")

    # Verificamos si ya se reveló el mensaje final para mostrar una felicitación especial
    if st.session_state.revelados[2][2]:
        st.snow()  # Efecto de copos cayendo
        st.markdown("""
            <div style="background-color:#2ecc71; padding:20px; border-radius:15px; text-align:center;">
                <h1 style="color:white; margin:0;">🎊 ¡LLEGÓ EL MOMENTO! 🎊</h1>
                <p style="color:white; font-size:20px;">Camilo y Angelica, el bebé es...</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Haz clic en los cuadros para descubrir qué hay detrás.")

    for i in range(3):
        cols = st.columns(3, gap="small")
        for j in range(3):
            border_css = obtener_bordes(i, j)

            if st.session_state.revelados[i][j]:
                res = revelacion_map[(i, j)]
                # Color especial para el mensaje final
                if res == "Dinos cuál es":
                    color = "#2ecc71"  # Verde éxito
                    font_size = "22px"
                else:
                    color = "#3498db" if "Niño" in res else "#e74c3c"
                    font_size = "18px"

                cols[j].markdown(
                    f"<div style='height:100px; display:flex; align-items:center; justify-content:center; {border_css} background-color:transparent; color:{color}; font-weight:bold; font-size:{font_size}; text-align:center;'>{res}</div>",
                    unsafe_allow_html=True)
            else:
                # El mismo truco CSS de los bordes
                cols[j].markdown(f'''
                    <div class="rev-marker-{i}-{j}" style="display:none;"></div>
                    <style>
                    div.element-container:has(.rev-marker-{i}-{j}) + div.element-container .stButton > button {{
                        {border_css} height: 100px; border-radius: 0px !important; background-color: transparent !important;
                    }}
                    </style>
                ''', unsafe_allow_html=True)

                if cols[j].button("❓", key=f"rev_{i}{j}", use_container_width=True):
                    st.session_state.revelados[i][j] = True
                    st.rerun()

# --- VISTA 2: JUEGO NORMAL ---
else:
    st.title("👶 El bebé de Camilo & Angelica")

    if st.session_state.jugador1 is None:
        with st.expander("📖 ¿Cómo jugar? (Instrucciones)", expanded=True):
            st.write("""
            1. **Elige tu bando:** Selecciona si crees que el bebé será Niño o Niña.
            2. **El Triki:** El objetivo es completar una línea de 3 (horizontal, vertical o diagonal).
            3. **Turnos:** El juego alternará automáticamente entre Niño y Niña.
            4. **El Final:** Al terminar, ¡podrás acceder a la pantalla secreta de revelación!
            """)

        st.markdown("<h3 style='text-align: center;'>🤔 ¿Qué crees que será el bebé?</h3>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        if c1.button("💙 ¡Es Niño!", use_container_width=True):
            st.session_state.jugador1, st.session_state.turno = "Niño", "Niño"
            st.rerun()
        if c2.button("💗 ¡Es Niña!", use_container_width=True):
            st.session_state.jugador1, st.session_state.turno = "Niña", "Niña"
            st.rerun()

    else:
        st.subheader(f"Turno de: {st.session_state.turno}")

        for i in range(3):
            cols = st.columns(3, gap="small")
            for j in range(3):
                valor = st.session_state.tablero[i][j]
                border_css = obtener_bordes(i, j)

                if valor == "":
                    # Inyección del truco CSS para los cuadros vacíos
                    cols[j].markdown(f'''
                        <div class="juego-marker-{i}-{j}" style="display:none;"></div>
                        <style>
                        div.element-container:has(.juego-marker-{i}-{j}) + div.element-container .stButton > button {{
                            {border_css} height: 100px; border-radius: 0px !important; background-color: transparent !important;
                        }}
                        div.element-container:has(.juego-marker-{i}-{j}) + div.element-container .stButton > button:hover {{
                            background-color: #f0f2f6 !important;
                        }}
                        </style>
                    ''', unsafe_allow_html=True)

                    if cols[j].button(" ", key=f"juego_{i}{j}", use_container_width=True):
                        st.session_state.tablero[i][j] = st.session_state.turno
                        if verificar_ganador(st.session_state.tablero):
                            st.session_state.ganador = st.session_state.turno
                        elif all(all(c != "" for c in fila) for fila in st.session_state.tablero):
                            st.session_state.ganador = "Empate"
                        else:
                            st.session_state.turno = "Niña" if st.session_state.turno == "Niño" else "Niño"
                        st.rerun()
                else:
                    color = "#3498db" if valor == "Niño" else "#e74c3c"
                    cols[j].markdown(
                        f"<div style='height:100px; display:flex; align-items:center; justify-content:center; {border_css} background-color:transparent; color:{color}; font-size:28px; font-weight:bold;'>{valor}</div>",
                        unsafe_allow_html=True)

    if st.session_state.ganador:
        st.balloons()
        if st.session_state.ganador == "Empate":
            st.warning("🤝 Aún no sabemos ¡Es un Empate!")
        else:
            st.success(f"🎉 ¡Felicidades! Ganó el bando: {st.session_state.ganador}")

        col_res1, col_res2 = st.columns(2)
        if col_res1.button("🔄 Reiniciar", use_container_width=True):
            st.session_state.clear()
            st.rerun()
        if col_res2.button("🚀 MODO REVELACIÓN", use_container_width=True):
            st.session_state.modo_revelacion = True
            st.rerun()



