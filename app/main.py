import streamlit as st

from app.model import predecir
from app.moderation import (
    es_toxico,
    censurar_comentario,
    requiere_alerta_baneo
)

st.set_page_config(
    page_title="Vigía | Blog",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ Vigía")
st.subheader("Blog con moderación inteligente de comentarios")

st.caption(
    "Sistema experimental de detección de comentarios tóxicos con BERT."
)

# Datos temporales de demostración
if "comentarios" not in st.session_state:
    st.session_state.comentarios = []

if "reincidencias" not in st.session_state:
    st.session_state.reincidencias = {}

if "ultimo_analisis" not in st.session_state:
    st.session_state.ultimo_analisis = None

st.info(
    "Modelo entrenado principalmente en inglés. "
    "Los resultados en español no son fiables."
)

usuarios = ["usuario_01", "usuario_02", "usuario_03"]

usuario = st.selectbox(
    "Usuario de demostración",
    usuarios
)

st.divider()

st.header("Publicación")

with st.form("form_comentario", clear_on_submit=True):

    texto = st.text_area(
        "Escribe tu comentario",
        placeholder="Comparte tu opinión...",
        height=120
    )

    publicar = st.form_submit_button("Publicar comentario")

if publicar:

    try:
        resultado = predecir(texto)

        toxicidad = es_toxico(resultado)

        if usuario not in st.session_state.reincidencias:
            st.session_state.reincidencias[usuario] = 0

        if toxicidad:

            st.session_state.reincidencias[usuario] += 1

            texto_visible = censurar_comentario(
                texto,
                resultado
            )

        else:
            texto_visible = texto

        infracciones = st.session_state.reincidencias[usuario]

        st.session_state.comentarios.append({
            "usuario": usuario,
            "texto": texto_visible,
            "toxicity": toxicidad,
            "probabilidad": resultado["prob_toxico"]
        })

        st.session_state.ultimo_analisis = {
            "resultado": resultado,
            "infracciones": infracciones,
            "toxicity": toxicidad
        }

        if toxicidad:
            st.error("Comentario censurado por posible toxicidad.")
        else:
            st.success("Comentario publicado correctamente.")

    except ValueError as error:
        st.warning(str(error))

    except Exception as error:
        st.error(f"No fue posible ejecutar el análisis: {error}")


# Mostrar análisis del último comentario
analisis = st.session_state.ultimo_analisis

if analisis:

    resultado = analisis["resultado"]

    st.divider()
    st.header("Análisis de BERT")

    st.write("Clasificación:", resultado["etiqueta"])

    st.metric(
        "Probabilidad de toxicidad",
        f"{resultado['prob_toxico']:.2%}"
    )

    st.progress(resultado["prob_toxico"])

    st.write("Umbral:", resultado["umbral"])

    st.write(
        "Confianza:",
        f"{resultado['confianza']:.2%}"
    )

    st.write(
        "Infracciones del usuario:",
        analisis["infracciones"]
    )

    if requiere_alerta_baneo(analisis["infracciones"]):
        st.error(
            "ALERTA: posible suspensión de cuenta "
            "por reiteración de comentarios tóxicos."
        )

    if analisis["toxicity"]:
        st.warning("El comentario completo fue censurado.")

st.divider()

st.header("Comentarios del blog")

if not st.session_state.comentarios:
    st.info("Todavía no hay comentarios.")

for comentario in reversed(st.session_state.comentarios):

    st.write(f"**{comentario['usuario']}**")

    if comentario["toxicity"]:
        st.error("[COMENTARIO CENSURADO]")
    else:
        st.write(comentario["texto"])
