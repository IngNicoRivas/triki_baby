import streamlit as st

st.set_page_config(page_title="El bebé de Camilo & Angelica", layout="centered")

# --- ESTILO CSS PERSONALIZADO ---
st.markdown("""
    <style>
    .main {
        background-color: #fdfaf5;
    }
    .stButton>button {
        border-radius: 20px;
        border: 2px solid #f0f2f6;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        border-color: #ffb7c5;
        transform: scale(1.02);
    }
    /* Aviso para celulares */
    @media only screen and (max-width: 600px) {
        .mobile-warn {
            background-color: #fff3cd;
            color: #856404;
            padding: 10px;
            border-radius: 5px;
            text-align: center;
            margin-bottom: 15px;
            font-weight: bold;
        }
    }
    @media only screen and (min-width: 601px) {
        .mobile-warn { display: none; }
    }
    </style>
    """, unsafe_allow_html=True)

if "tablero" not in st.session_state:
    st.session_state.tablero = [["" for _ in range(3)] for _ in range(3)]
    st.session_state.turno = None
    st.session_state.jugador1 = None
    st.session_state.jugador2 = None
    st.session_state.ganador = None
    st.session_state.modo_revelacion = False
    st.session_state.revelados = [[False for _ in range(3)] for _ in range(3)]

revelacion_map = {
    (0,0): "Niño", (1,1): "Niño", (2,0): "Niño", (2,1): "Niño",
    (0,2): "Niña", (1,2): "Niña", (1,0): "Niña", (0,1): "Niña",
    (2,2): "¡Abre el sobre!"
}

def verificar_ganador(tablero):
    for i in range(3):
        if tablero[i][0] == tablero[i][1] == tablero[i][2] != "":
            return True
        if tablero[0][i] == tablero[1][i] == tablero[2][i] != "":
            return True
    if tablero[0][0] == tablero[1][1] == tablero[2][2] != "":
        return True
    if tablero[0][2] == tablero[1][1] == tablero[2][0] != "":
        return True
    return False

st.markdown('<div class="mobile-warn">📱 Desde celular por favor, girarlo de forma horizontal 🔄</div>', unsafe_allow_html=True)

# --- VISTA 1: MODO REVELACIÓN ---
if st.session_state.modo_revelacion:
    st.title("🕵️‍♂️ Descubre el ganador")
    st.info("Haz clic en los cuadros para descubrir qué hay detrás de cada posición.")

    for i in range(3):
        cols = st.columns(3)
        for j in range(3):
            # Si el botón ya fue pulsado, mostramos el texto
            if st.session_state.revelados[i][j]:
                resultado = revelacion_map[(i, j)]
                color = "#3498db" if "Niño" in resultado else "#e74c3c" if "Niña" in resultado else "#2ecc71"
                cols[j].markdown(
                    f"<div style='text-align:center; color:{color}; font-weight:bold; height:45px; display:flex; align-items:center; justify-content:center; border:1px solid #eee; border-radius:5px;'>{resultado}</div>",
                    unsafe_allow_html=True
                )
            # Si no ha sido pulsado, mostramos el botón con "?"
            else:
                if cols[j].button("❓", key=f"rev_{i}{j}", use_container_width=True):
                    st.session_state.revelados[i][j] = True
                    st.rerun()

    st.write("---")
    if st.button("⬅️ Volver al juego principal"):
        st.session_state.modo_revelacion = False
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
        st.write("<p style='text-align: center; color: gray;'>Selecciona tu predicción para empezar a jugar:</p>",unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💙 ¡Es Niño!", use_container_width=True):
                st.session_state.jugador1, st.session_state.turno = "Niño", "Niño"
                st.rerun()
        with col2:
            if st.button("💗 ¡Es Niña!", use_container_width=True):
                st.session_state.jugador1, st.session_state.turno = "Niña", "Niña"
                st.rerun()

    else:
        st.subheader(f"Turno de: {st.session_state.turno}")
        for i in range(3):
            cols = st.columns(3)
            for j in range(3):
                valor = st.session_state.tablero[i][j]
                if valor == "":
                    if cols[j].button(" ", key=f"juego_{i}{j}", use_container_width=True):
                        st.session_state.tablero[i][j] = st.session_state.turno
                        if verificar_ganador(st.session_state.tablero):
                            st.session_state.ganador = st.session_state.turno
                        elif all(all(c != "" for c in fila) for fila in st.session_state.tablero):
                            st.session_state.ganador = "Aún no sabemos es Empate!"
                        else:
                            st.session_state.turno = "Niña" if st.session_state.turno == "Niño" else "Niño"
                        st.rerun()
                else:
                    color = "blue" if valor == "Niño" else "red"
                    cols[j].markdown(f"<div style='text-align:center; color:{color}; font-weight:bold;'>{valor}</div>", unsafe_allow_html=True)

    if st.session_state.ganador:
        st.success(f"🎉 ¡Felicidades! Ganó el bando: {st.session_state.ganador}")
        c1, c2 = st.columns(2)
        if c1.button("Volver a Jugar"):
            st.session_state.clear() # Limpia todo para empezar de cero
            st.rerun()
        if c2.button("🚀 Ir al Modo Revelación"):
            st.session_state.modo_revelacion = True
            st.rerun()


