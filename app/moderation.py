UMBRAL_REINCIDENCIA = 3


def es_toxico(resultado):
    return resultado["prob_toxico"] >= resultado["umbral"]


def censurar_comentario(texto, resultado):

    if es_toxico(resultado):
        return "[COMENTARIO CENSURADO]"

    return texto


def requiere_alerta_baneo(reincidencias):

    return reincidencias >= UMBRAL_REINCIDENCIA
