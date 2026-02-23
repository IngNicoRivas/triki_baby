import streamlit as st

st.set_page_config(page_title="El bebé de Camilo & Angelica", layout="centered")

if "tablero" not in st.session_state:
    st.session_state.tablero = [["" for _ in range(3)] for _ in range(3)]
    st.session_state.turno = None
    st.session_state.jugador1 = None
    st.session_state.jugador2 = None
    st.session_state.ganador = None


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

st.title("👶 El bebé de Camilo & Angelica")

if st.session_state.jugador1 is None:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Niño", use_container_width=True):
            st.session_state.jugador1 = "Niño"
            st.session_state.jugador2 = "Niña"
            st.session_state.turno = "Niño"
            st.rerun()
    with col2:
        if st.button("Niña", use_container_width=True):
            st.session_state.jugador1 = "Niña"
            st.session_state.jugador2 = "Niño"
            st.session_state.turno = "Niña"
            st.rerun()

else:
    st.subheader(f"Turno de {st.session_state.turno}")

    for i in range(3):
        cols = st.columns(3)
        for j in range(3):
            valor = st.session_state.tablero[i][j]
            if valor == "":
                if cols[j].button(" ", key=f"{i}{j}", use_container_width=True):
                    st.session_state.tablero[i][j] = st.session_state.turno
                    if verificar_ganador(st.session_state.tablero):
                        st.session_state.ganador = st.session_state.turno
                    elif all(all(c != "" for c in fila) for fila in st.session_state.tablero):
                        st.session_state.ganador = "Empate"
                    else:
                        st.session_state.turno = (
                            st.session_state.jugador1
                            if st.session_state.turno == st.session_state.jugador2
                            else st.session_state.jugador2
                        )
                    st.rerun()
            else:
                color = "blue" if valor == "Niño" else "red"
                cols[j].markdown(
                    f"<div style='text-align:center; color:{color}; font-weight:bold;'>{st.session_state.tablero[i][j]}</div>",
                    unsafe_allow_html=True,
                )


if st.session_state.ganador:
    if st.session_state.ganador == "Empate":
        st.success("🤝 Aún no sabemos ¡Empate!")
    else:
        st.success(f"🎉 FELICITACIONES Camilo y Angelica ¡El bebé es: {st.session_state.ganador}!")
    if st.button("Reiniciar juego"):
        st.session_state.tablero = [["" for _ in range(3)] for _ in range(3)]
        st.session_state.turno = None
        st.session_state.jugador1 = None
        st.session_state.jugador2 = None
        st.session_state.ganador = None
        st.rerun()
