
import streamlit as st

from app.model import (
    predecir,
    ErrorEntrada
)

from app.database import (
    inicializar_db,
    obtener_usuario,
    obtener_comentarios,
    obtener_historial,
    obtener_usuarios
)

from app.moderation import moderar_comentario


# ==========================================
# CONFIGURACION
# ==========================================

st.set_page_config(
    page_title="Vigía | Blog inteligente",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

inicializar_db()


# ==========================================
# ESTILOS
# ==========================================

st.markdown("""
<style>

.stApp {
    background-color: #f5f7fb;
}

.main-title {
    font-size: 38px;
    font-weight: 800;
    color: #172554;
}

.subtitle {
    color: #64748b;
    font-size: 16px;
}

.post-card {
    background: white;
    padding: 22px;
    border-radius: 14px;
    border: 1px solid #e2e8f0;
    margin-bottom: 15px;
}

.metric-card {
    background: white;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #e2e8f0;
}

.comment-card {
    background: white;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #e2e8f0;
    margin-bottom: 10px;
}

.small-text {
    color: #64748b;
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# CABECERA
# ==========================================

col1, col2 = st.columns([4, 1])

with col1:

    st.markdown(
        '<div class="main-title">🛡️ Vigía</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Comunidad digital con moderación inteligente '
        'mediante inteligencia artificial.'
        '</div>',
        unsafe_allow_html=True
    )

with col2:

    st.markdown("### BERT")

    st.success("Sistema activo")


st.divider()


# ==========================================
# ADVERTENCIA DEL MODELO
# ==========================================

st.warning(
    "Modelo experimental entrenado principalmente en inglés. "
    "Su rendimiento en español no está validado. "
    "Los resultados deben interpretarse como apoyo a la moderación."
)


# ==========================================
# MENU LATERAL
# ==========================================

st.sidebar.title("Panel Vigía")

pagina = st.sidebar.radio(
    "Navegación",
    [
        "Blog",
        "Análisis inteligente",
        "Panel de moderación"
    ]
)

st.sidebar.divider()

st.sidebar.caption(
    "EV1 - Prototipo de detección de comentarios tóxicos"
)


# ==========================================
# PAGINA 1: BLOG
# ==========================================

if pagina == "Blog":

    st.header("Publicaciones de la comunidad")

    st.markdown("""
    <div class="post-card">
        <h3>💻 Tecnología y sociedad</h3>
        <p>
        ¿Cómo está cambiando la inteligencia artificial
        nuestra forma de comunicarnos?
        Comparte tu opinión con la comunidad.
        </p>
        <span class="small-text">Publicado por Vigía</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="post-card">
        <h3>🌐 Internet y convivencia digital</h3>
        <p>
        La convivencia en internet depende de la
        participación responsable de todos.
        ¿Qué medidas mejorarían las comunidades digitales?
        </p>
        <span class="small-text">Publicado por Vigía</span>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.subheader("Escribir un comentario")

    usuarios = obtener_usuarios()

    nombres = [
        usuario["nombre"]
        for usuario in usuarios
    ]

    usuario = st.selectbox(
        "Identidad de demostración",
        nombres
    )

    with st.form(
        "formulario_comentario",
        clear_on_submit=True
    ):

        texto = st.text_area(
            "Tu comentario",
            placeholder="Escribe tu opinión aquí...",
            height=120
        )

        enviar = st.form_submit_button(
            "Publicar comentario",
            use_container_width=True
        )

    if enviar:

        if not texto.strip():

            st.warning("Debes escribir un comentario.")

        else:

            with st.spinner(
                "BERT está analizando el comentario..."
            ):

                try:

                    resultado = predecir(texto)

                    moderacion = moderar_comentario(
                        usuario,
                        texto,
                        resultado
                    )

                    st.session_state["ultimo_resultado"] = {
                        "resultado": resultado,
                        "moderacion": moderacion
                    }

                    st.session_state["pagina_resultado"] = True

                except ErrorEntrada as error:

                    st.error(
                        f"Entrada inválida: {error}"
                    )

                except Exception as error:

                    st.error(
                        f"No fue posible procesar el comentario: {error}"
                    )

    # --------------------------------------
    # RESULTADO DE LA PUBLICACION
    # --------------------------------------

    if st.session_state.get("pagina_resultado"):

        datos = st.session_state["ultimo_resultado"]

        resultado = datos["resultado"]

        moderacion = datos["moderacion"]

        st.divider()

        st.subheader("Resultado de moderación")

        if moderacion["toxico"]:

            st.error(
                "🚫 Comentario censurado. "
                "El sistema detectó posible toxicidad."
            )

        else:

            st.success(
                "✅ Comentario publicado correctamente."
            )

        # Probabilidad
        st.metric(
            "Probabilidad de toxicidad",
            f"{resultado['prob_toxico']:.2%}"
        )

        st.progress(
            resultado["prob_toxico"]
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Clasificación",
            resultado["etiqueta"]
        )

        col2.metric(
            "Confianza",
            f"{resultado['confianza']:.2%}"
        )

        col3.metric(
            "Umbral",
            f"{resultado['umbral']:.2%}"
        )

        st.info(
            f"Usuario: {moderacion['usuario']}"
        )

        st.write(
            "Comentario:",
            moderacion["contenido"]
        )

        st.write(
            "Infracciones acumuladas:",
            moderacion["infracciones"]
        )

        if moderacion["alerta_baneo"]:

            st.error(
                "⚠️ ALERTA: el usuario alcanzó tres "
                "infracciones. Se recomienda revisar "
                "su cuenta para una posible suspensión."
            )

        elif moderacion["toxico"]:

            restantes = (
                3 - moderacion["infracciones"]
            )

            st.warning(
                f"Advertencia registrada. "
                f"Faltan {restantes} infracciones "
                "para activar la alerta de posible suspensión."
            )

        for aviso in resultado["advertencias"]:

            st.warning(aviso)

        with st.expander("Detalles técnicos del análisis"):

            st.write(
                "Probabilidad tóxica:",
                resultado["prob_toxico"]
            )

            st.write(
                "Confianza:",
                resultado["confianza"]
            )

            st.write(
                "Umbral:",
                resultado["umbral"]
            )

            st.write(
                resultado["limitacion"]
            )

    # --------------------------------------
    # COMENTARIOS PUBLICADOS
    # --------------------------------------

    st.divider()

    st.subheader("Comentarios de la comunidad")

    comentarios = obtener_comentarios()

    if not comentarios:

        st.info(
            "Todavía no existen comentarios publicados."
        )

    for comentario in comentarios:

        with st.container(border=True):

            st.markdown(
                f"**{comentario['usuario']}**"
            )

            if comentario["es_toxico"]:

                st.error(
                    "[COMENTARIO CENSURADO]"
                )

            else:

                st.write(
                    comentario["contenido"]
                )

            st.caption(
                f"Fecha: {comentario['fecha']}"
            )


# ==========================================
# PAGINA 2: ANALISIS INTELIGENTE
# ==========================================

elif pagina == "Análisis inteligente":

    st.header("Análisis del modelo BERT")

    st.write(
        "Esta sección permite evaluar un comentario "
        "sin publicarlo en el blog."
    )

    texto_prueba = st.text_area(
        "Comentario para analizar",
        height=150
    )

    if st.button(
        "Analizar comentario",
        use_container_width=True
    ):

        try:

            resultado = predecir(texto_prueba)

            st.subheader("Resultado")

            st.write(
                "Clasificación:",
                resultado["etiqueta"]
            )

            st.metric(
                "Probabilidad de toxicidad",
                f"{resultado['prob_toxico']:.2%}"
            )

            st.progress(
                resultado["prob_toxico"]
            )

            st.write(
                "Confianza:",
                f"{resultado['confianza']:.2%}"
            )

            st.write(
                "Umbral:",
                resultado["umbral"]
            )

            for aviso in resultado["advertencias"]:

                st.warning(aviso)

            with st.expander("Limitaciones"):

                st.write(resultado["limitacion"])

        except ErrorEntrada as error:

            st.error(str(error))

        except Exception as error:

            st.error(
                f"Error al ejecutar el modelo: {error}"
            )


# ==========================================
# PAGINA 3: PANEL DE MODERACION
# ==========================================

elif pagina == "Panel de moderación":

    st.header("Panel de moderación")

    usuarios = obtener_usuarios()

    comentarios = obtener_comentarios()

    historial = obtener_historial()

    total_comentarios = len(comentarios)

    total_toxicos = sum(
        comentario["es_toxico"]
        for comentario in comentarios
    )

    total_normales = (
        total_comentarios - total_toxicos
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Comentarios analizados",
        total_comentarios
    )

    col2.metric(
        "Comentarios tóxicos",
        total_toxicos
    )

    col3.metric(
        "Comentarios publicados",
        total_normales
    )

    st.divider()

    st.subheader("Usuarios y reincidencias")

    for usuario in usuarios:

        with st.container(border=True):

            col1, col2, col3 = st.columns(3)

            col1.write(
                f"**{usuario['nombre']}**"
            )

            col2.metric(
                "Infracciones",
                usuario["infracciones"]
            )

            if usuario["infracciones"] >= 3:

                col3.error(
                    "Posible suspensión"
                )

            elif usuario["infracciones"] > 0:

                col3.warning(
                    "Advertido"
                )

            else:

                col3.success(
                    "Sin infracciones"
                )

    st.divider()

    st.subheader("Historial de moderación")

    if not historial:

        st.info(
            "No existen registros de moderación."
        )

    else:

        for registro in historial:

            with st.container(border=True):

                col1, col2 = st.columns(2)

                col1.write(
                    f"**{registro['usuario']}**"
                )

                col2.caption(
                    registro["fecha"]
                )

                st.write(
                    "Clasificación:",
                    registro["clasificacion"]
                )

                st.write(
                    "Probabilidad:",
                    f"{registro['probabilidad']:.2%}"
                )

                st.write(
                    "Infracciones:",
                    registro["infracciones"]
                )

                if registro["censurado"]:

                    st.error(
                        "Comentario censurado"
                    )

                else:

                    st.success(
                        "Comentario publicado"
                    )

    st.divider()

    st.caption(
        "La alerta de suspensión es una simulación "
        "de una regla de moderación. No se ejecuta "
        "un baneo automático."
    )
