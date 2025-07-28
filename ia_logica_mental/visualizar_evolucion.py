import json
from pathlib import Path
import streamlit as st
import matplotlib.pyplot as plt

def mostrar_graficos():
    HISTORIAL_FILE = Path("experiencias_historial.json")
    
    if not HISTORIAL_FILE.exists():
        st.warning("No hay historial aún para visualizar.")
        return

    with open(HISTORIAL_FILE, "r") as f:
        historial = json.load(f)

    sust = []
    gan = []
    bombeo = []
    produccion = []

    for juego in historial:
        for ronda in juego[1:-1]:  # Excluye valores_iniciales y valores_finales
            resultado = ronda.get("resultado", {})
            decision = ronda.get("decision", {})

            sust.append(resultado.get("indice_sustentabilidad", None))
            gan.append(resultado.get("indice_ganancias", None))
            bombeo.append(decision.get("fraccion_bombeo", None))
            produccion.append(decision.get("produccion_planeada", None))

    if not sust:
        st.info("No hay suficientes datos aún.")
        return

    x = list(range(1, len(sust) + 1))

    st.subheader("📈 Evolución ronda a ronda")
    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(x, sust, label="Índice de Sustentabilidad", color="green", linestyle="--")
    ax.plot(x, gan, label="Índice de Ganancias", color="orange", linestyle="--")
    ax.plot(x, bombeo, label="Fracción de Bombeo", color="blue", linestyle="--")
    ax.plot(x, produccion, label="Producción Planeada", color="purple", linestyle="--")

    ax.set_xlabel("Ronda total acumulada")
    ax.set_ylabel("Valores")
    ax.set_title("Evolución de decisiones y resultados")
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)
