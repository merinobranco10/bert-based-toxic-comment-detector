import os
import torch
import streamlit as st

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification
)

MODEL_ID = os.getenv(
    "HF_MODEL_ID",
    "TU_USUARIO/vigia-bert-toxicidad"
)

UMBRAL = 0.5
MAX_LENGTH = 256


@st.cache_resource
def cargar_modelo():

    if MODEL_ID.startswith("TU_USUARIO"):
        raise RuntimeError("Configura tu repositorio de Hugging Face.")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)

    modelo = AutoModelForSequenceClassification.from_pretrained(
        MODEL_ID
    )

    dispositivo = torch.device(
        "cuda" if torch.cuda.is_available() else "cpu"
    )

    modelo.to(dispositivo)
    modelo.eval()

    return tokenizer, modelo, dispositivo


def predecir(texto):

    if not isinstance(texto, str):
        raise ValueError("El comentario debe ser texto.")

    texto = texto.strip()

    if len(texto) < 3 or len(texto) > 5000:
        raise ValueError("El comentario debe tener entre 3 y 5000 caracteres.")

    tokenizer, modelo, dispositivo = cargar_modelo()

    entradas = tokenizer(
        texto,
        truncation=True,
        max_length=MAX_LENGTH,
        return_tensors="pt"
    ).to(dispositivo)

    with torch.inference_mode():
        logits = modelo(**entradas).logits
        probabilidades = torch.softmax(logits, dim=-1)[0]

    # Obtener el índice de la etiqueta tóxica
    label2id = modelo.config.label2id

    id_toxico = next(
        (
            int(idx)
            for label, idx in label2id.items()
            if "tox" in label.lower()
        ),
        1
    )

    probabilidad = float(probabilidades[id_toxico].item())

    return {
        "etiqueta": (
            "Tóxico" if probabilidad >= UMBRAL
            else "No tóxico"
        ),
        "prob_toxico": round(probabilidad, 4),
        "confianza": round(
            max(probabilidad, 1 - probabilidad), 4
        ),
        "umbral": UMBRAL
    }
