import json
from pathlib import Path
import streamlit as st
import matplotlib.pyplot as plt

def mostrar_graficos():
    HISTORIAL_FILE = Path("experiencias_historial.json")
    
    if not HISTORIAL_FILE.exists():
        st.warning("No hay historial aún para visualizar.")
        return

    with open(HISTORIAL_FILE, "r", encoding="utf-8") as f:
        historial = json.load(f)

    sust = []
    gan = []
    bombeo = []
    produccion = []

    # Recorremos juegos y rondas (saltando valores_iniciales y valores_finales si existen)
    for juego in historial:
        for ronda in juego[1:-1]:
            resultado = ronda.get("resultado", {}) or {}
            decision = ronda.get("decision", {}) or {}

            sust.append(resultado.get("indice_sustentabilidad"))
            gan.append(resultado.get("indice_ganancias"))
            bombeo.append(decision.get("fraccion_bombeo"))
            produccion.append(decision.get("produccion_planeada"))

    # Validación de datos
    if not any([sust, gan, bombeo, produccion]) or len(sust) == 0:
        st.info("No hay suficientes datos aún.")
        return

    x = list(range(1, len(sust) + 1))

    st.subheader("📈 Evolución ronda a ronda")

    # === Gráfico 1: Índices (sustentabilidad y ganancias) ===
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    ax1.plot(x, sust, label="Índice de Sustentabilidad", color="green", linestyle="--")
    ax1.plot(x, gan, label="Índice de Ganancias", color="orange", linestyle="--")
    ax1.set_xlabel("Ronda total acumulada")
    ax1.set_ylabel("Índices")
    ax1.set_title("Evolución de Índices (Sustentabilidad y Ganancias)")
    ax1.legend()
    ax1.grid(True)
    st.pyplot(fig1)

    # === Gráfico 2: Decisiones (fracción de bombeo y producción planeada) ===
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    ax2.plot(x, bombeo, label="Fracción de Bombeo", color="blue", linestyle="--")
    ax2.plot(x, produccion, label="Producción Planeada", color="purple", linestyle="--")
    ax2.set_xlabel("Ronda total acumulada")
    ax2.set_ylabel("Valores")
    ax2.set_title("Evolución de Decisiones (Bombeo y Producción)")
    ax2.legend()
    ax2.grid(True)
    st.pyplot(fig2)
