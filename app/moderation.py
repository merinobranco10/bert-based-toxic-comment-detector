
from app.database import (
    registrar_moderacion
)


UMBRAL_REINCIDENCIA = 3

MARCADOR_CENSURA = "[COMENTARIO CENSURADO]"


def es_toxico(resultado):

    return (
        resultado["prob_toxico"]
        >= resultado["umbral"]
    )


def censurar_comentario(texto, resultado):

    if es_toxico(resultado):
        return MARCADOR_CENSURA

    return texto


def requiere_alerta_baneo(infracciones):

    return infracciones >= UMBRAL_REINCIDENCIA


def moderar_comentario(usuario, texto, resultado):

    toxicidad = es_toxico(resultado)

    contenido = censurar_comentario(
        texto,
        resultado
    )

    infracciones = registrar_moderacion(
        usuario=usuario,
        contenido=texto,
        es_toxico=toxicidad,
        probabilidad=resultado["prob_toxico"]
    )

    return {
        "usuario": usuario,
        "toxico": toxicidad,
        "contenido": contenido,
        "infracciones": infracciones,
        "alerta_baneo": requiere_alerta_baneo(
            infracciones
        )
    }
