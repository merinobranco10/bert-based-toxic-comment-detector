from app.moderation import (
    es_toxico,
    censurar_comentario,
    requiere_alerta_baneo
)


def test_detectar_toxicidad():
    resultado = {
        "prob_toxico": 0.90,
        "umbral": 0.5
    }

    assert es_toxico(resultado) is True


def test_comentario_no_toxico():
    resultado = {
        "prob_toxico": 0.10,
        "umbral": 0.5
    }

    assert es_toxico(resultado) is False


def test_censurar_comentario():
    resultado = {
        "prob_toxico": 0.90,
        "umbral": 0.5
    }

    mensaje = censurar_comentario(
        "Comentario de prueba",
        resultado
    )

    assert mensaje == "[COMENTARIO CENSURADO]"


def test_alerta_tercera_infraccion():
    assert requiere_alerta_baneo(3) is True


def test_sin_alerta_primera_infraccion():
    assert requiere_alerta_baneo(1) is False
