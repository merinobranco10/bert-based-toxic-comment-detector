import os
import re

import torch
import streamlit as st

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification
)


# ==========================================
# CONFIGURACION DEL MODELO
# ==========================================

MODEL_ID = os.getenv(
    "HF_MODEL_ID",
    "bmerino10/vigia-bert-toxicidad"
)

MAX_LENGTH = 256
UMBRAL = 0.5
MAX_CARACTERES = 5000
MIN_CARACTERES = 3

ID_TOXICO = 1

PALABRAS_ES = {
    "el", "la", "los", "las", "de", "del", "que",
    "y", "en", "un", "una", "por", "con", "para",
    "se", "muy", "pero", "esto", "eres", "está",
    "como", "qué", "tú", "eso", "lo"
}

LIMITACION = (
    "Modelo entrenado con Civil Comments, principalmente "
    "en inglés. Su fiabilidad no está validada para español. "
    "Puede equivocarse con ironía, contexto y expresiones "
    "ambiguas. No sustituye la revisión humana."
)


class ErrorEntrada(ValueError):
    """Error producido por una entrada inválida."""


# ==========================================
# CARGAR MODELO UNA SOLA VEZ
# ==========================================

@st.cache_resource
def cargar_modelo():

    if MODEL_ID.startswith("TU_USUARIO"):
        raise RuntimeError(
            "Debes configurar HF_MODEL_ID con tu usuario de Hugging Face."
        )

    dispositivo = torch.device(
        "cuda" if torch.cuda.is_available() else "cpu"
    )

    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)

    modelo = AutoModelForSequenceClassification.from_pretrained(
        MODEL_ID
    )

    modelo.to(dispositivo)
    modelo.eval()

    for parametro in modelo.parameters():
        parametro.requires_grad_(False)

    if modelo.config.num_labels != 2:
        raise RuntimeError(
            "El modelo debe tener exactamente dos clases."
        )

    return tokenizer, modelo, dispositivo


# ==========================================
# VALIDACION DE ENTRADAS
# ==========================================

def validar_entrada(texto, tokenizer):

    if texto is None:
        raise ErrorEntrada(
            "Falta el comentario."
        )

    if not isinstance(texto, str):
        raise ErrorEntrada(
            "El comentario debe ser texto."
        )

    limpio = texto.strip()

    if not limpio:
        raise ErrorEntrada(
            "El comentario está vacío."
        )

    if len(limpio) < MIN_CARACTERES:
        raise ErrorEntrada(
            "El comentario debe tener al menos 3 caracteres."
        )

    if len(limpio) > MAX_CARACTERES:
        raise ErrorEntrada(
            "El comentario supera los 5000 caracteres."
        )

    if not re.search(r"[A-Za-zÁÉÍÓÚáéíóúÑñ]", limpio):
        raise ErrorEntrada(
            "El comentario debe contener letras."
        )

    advertencias = []

    palabras = re.findall(
        r"\w+",
        limpio.lower()
    )

    coincidencias = sum(
        palabra in PALABRAS_ES
        for palabra in palabras
    )

    if coincidencias >= 2:

        advertencias.append(
            "El comentario parece estar en español. "
            "La fiabilidad del modelo no está validada para este idioma."
        )

    tokens = tokenizer(
        limpio,
        truncation=False,
        verbose=False
    )["input_ids"]

    if len(tokens) > MAX_LENGTH:

        advertencias.append(
            f"El comentario tiene {len(tokens)} tokens "
            f"y será truncado a {MAX_LENGTH}."
        )

    return limpio, advertencias


# ==========================================
# PREDICCION BERT
# ==========================================

def predecir(texto):

    tokenizer, modelo, dispositivo = cargar_modelo()

    texto_limpio, advertencias = validar_entrada(
        texto,
        tokenizer
    )

    entradas = tokenizer(
        texto_limpio,
        truncation=True,
        max_length=MAX_LENGTH,
        return_tensors="pt"
    ).to(dispositivo)

    with torch.inference_mode():

        logits = modelo(**entradas).logits

        probabilidades = torch.softmax(
            logits,
            dim=-1
        )[0].cpu()

    probabilidad = float(
        probabilidades[ID_TOXICO].item()
    )

    es_toxico = probabilidad >= UMBRAL

    confianza = (
        probabilidad
        if es_toxico
        else 1 - probabilidad
    )

    return {
        "etiqueta": (
            "Tóxico" if es_toxico
            else "No tóxico"
        ),

        "prob_toxico": round(
            probabilidad, 4
        ),

        "confianza": round(
            confianza, 4
        ),

        "umbral": UMBRAL,

        "advertencias": advertencias,

        "limitacion": LIMITACION
    }
