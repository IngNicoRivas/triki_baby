import streamlit as st

st.set_page_config(page_title="El bebé de Camilo & Angelica", layout="centered")

# --- ESTILO CSS GLOBAL Y TRUCO PARA UNIR EL TABLERO ---
st.markdown("""
    <style>
    .main {
        background-color: #fdfaf5;
    }
    .stButton>button {
        border-radius: 20px;
        transition: all 0.3s;
    }

    /* TRUCO PARA EL TABLERO PERFECTO (#) */
    div:has(> .marcador-tablero) [data-testid="stHorizontalBlock"] {
        gap: 0rem !important;
    }
    div:has(> .marcador-tablero) [data-testid="column"] {
        padding: 0 !important;
    }
    div:has(> .marcador-tablero) .element-container {
        margin-bottom: 0px !important;
    }

    @media only screen and (max-width: 600px) {
        .mobile-warn { background-color: #fff3cd; color: #856404; padding: 10px; border-radius: 5px; text-align: center; margin-bottom: 15px; font-weight: bold; }
    }
    @media only screen and (min-width: 601px) {
        .mobile-warn { display: none; }
    }
    </style>
    """, unsafe_allow_html=True)


# --- FUNCIÓN PARA LAS LÍNEAS DEL GRID (#) ---
def obtener_bordes(i, j):
    css = ""
    grosor = "5px"
    color_linea = "#2c3e50"

    if i < 2: css += f"border-bottom: {grosor} solid {color_linea} !important; "
    if j < 2: css += f"border-right: {grosor} solid {color_linea} !important; "

    return css


# --- ESTADO DE LA SESIÓN ---
if "tablero" not in st.session_state:
    st.session_state.tablero = [["" for _ in range(3)] for _ in range(3)]
    st.session_state.turno = None
    st.session_state.jugador1 = None
    st.session_state.ganador = None


def verificar_ganador(tablero):
    for i in range(3):
        if tablero[i][0] == tablero[i][1] == tablero[i][2] != "": return True
        if tablero[0][i] == tablero[1][i] == tablero[2][i] != "": return True
    if tablero[0][0] == tablero[1][1] == tablero[2][2] != "": return True
    if tablero[0][2] == tablero[1][1] == tablero[2][0] != "": return True
    return False


# --- MATRIZ DE LETRAS GUÍA (A-I para 9 casillas) ---
letras_guia = [
    ["A", "B", "C"],
    ["D", "E", "F"],
    ["G", "H", "I"]
]

st.markdown(
    '<div class="mobile-warn">📱 Para una mejor experiencia, gira tu celular de forma horizontal (Landscape) 🔄</div>',
    unsafe_allow_html=True)

st.title("👶 El bebé de Camilo & Angelica")

# --- MENÚ PRINCIPAL ---
if st.session_state.jugador1 is None:
    with st.expander("📖 ¿Cómo jugar? (Instrucciones)", expanded=True):
        st.write(
            "1. **Elige tu bando:** Selecciona si crees que será Niño o Niña.\n2. **El Triki:** Completa una línea de 3.\n3. **Turnos:** Se alternará automáticamente.")

    st.markdown("<h3 style='text-align: center;'>🤔 ¿Qué crees que será el bebé?</h3>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    if c1.button("💙 ¡Es Niño!", use_container_width=True):
        st.session_state.jugador1, st.session_state.turno = "Niño", "Niño"
        st.rerun()
    if c2.button("💗 ¡Es Niña!", use_container_width=True):
        st.session_state.jugador1, st.session_state.turno = "Niña", "Niña"
        st.rerun()

# --- JUEGO EN CURSO ---
else:
    # Mensaje de turno centrado
    st.markdown(
        f"<h3 style='text-align: center; color: #555;'>Turno del bando: <span style='color: {'#3498db' if st.session_state.turno == 'Niño' else '#e74c3c'};'>{st.session_state.turno}</span></h3>",
        unsafe_allow_html=True)

    # Marcador oculto para unir las celdas del juego
    st.markdown('<div class="marcador-tablero"></div>', unsafe_allow_html=True)

    for i in range(3):
        cols = st.columns(3)
        for j in range(3):
            valor = st.session_state.tablero[i][j]
            border_css = obtener_bordes(i, j)
            letra = letras_guia[i][j]

            if valor == "":
                # Botón con letra guía en color gris claro
                cols[j].markdown(f'''
                    <div class="juego-marker-{i}-{j}" style="display:none;"></div>
                    <style>
                    div.element-container:has(.juego-marker-{i}-{j}) + div.element-container .stButton > button {{
                        {border_css} height: 110px; border-radius: 0px !important; background-color: transparent !important; margin: 0 !important;
                        color: #bdc3c7 !important; font-size: 24px !important; font-weight: normal;
                    }}
                    div.element-container:has(.juego-marker-{i}-{j}) + div.element-container .stButton > button:hover {{
                        background-color: #f0f2f6 !important; color: #7f8c8d !important;
                    }}
                    </style>
                ''', unsafe_allow_html=True)

                if cols[j].button(letra, key=f"juego_{i}{j}", use_container_width=True):
                    st.session_state.tablero[i][j] = st.session_state.turno
                    if verificar_ganador(st.session_state.tablero):
                        st.session_state.ganador = st.session_state.turno
                    elif all(all(c != "" for c in fila) for fila in st.session_state.tablero):
                        st.session_state.ganador = "Empate"
                    else:
                        st.session_state.turno = "Niña" if st.session_state.turno == "Niño" else "Niño"
                    st.rerun()
            else:
                # Celda con la jugada (Niño/Niña)
                color = "#3498db" if valor == "Niño" else "#e74c3c"
                cols[j].markdown(
                    f"<div style='height:110px; display:flex; align-items:center; justify-content:center; {border_css} background-color:transparent; color:{color}; font-size:32px; font-weight:bold; margin:0;'>{valor}</div>",
                    unsafe_allow_html=True)

# --- FINAL DEL JUEGO ---
if st.session_state.ganador:
    st.balloons()
    if st.session_state.ganador == "Empate":
        st.warning("🤝 Aún no sabemos ¡Es un Empate!")
    else:
        st.success(f"🎉 ¡Felicidades! Ganó el bando: {st.session_state.ganador}")

    if st.button("🔄 Reiniciar Juego", use_container_width=True):
        st.session_state.clear()
        st.rerun()

