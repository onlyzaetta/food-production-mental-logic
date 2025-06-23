import json
from pathlib import Path

PARAMS_FILE = Path("parametros_aprendidos.json")
HISTORIAL_FILE = Path("experiencias_historial.json")

def get_parametros_default():
    return {
        "fraccion_bombeo_base": 0.5,
        "produccion_planeada_base": 900
    }

def cargar_parametros():
    if PARAMS_FILE.exists():
        with open(PARAMS_FILE, 'r') as f:
            return json.load(f)
    return get_parametros_default()

def guardar_parametros(parametros):
    with open(PARAMS_FILE, 'w') as f:
        json.dump(parametros, f, indent=4)

def evaluar_eficacia(valores_iniciales, valores_finales):
    """
    Retorna una puntuación de eficacia comparando valores_iniciales y valores_finales.
    Penaliza si el índice de sustentabilidad o ganancias bajan.
    """
    sust_ini = valores_iniciales.get("indice_sustentabilidad")
    sust_fin = valores_finales.get("indice_sustentabilidad")
    gan_ini = valores_iniciales.get("indice_ganancias")
    gan_fin = valores_finales.get("indice_ganancias")

    score = 0
    if sust_ini is not None and sust_fin is not None:
        score += (sust_fin - sust_ini)
    if gan_ini is not None and gan_fin is not None:
        score += (gan_fin - gan_ini)

    return score

def ajustar_parametros():
    if not HISTORIAL_FILE.exists():
        print("No hay historial para ajustar parámetros.")
        return

    with open(HISTORIAL_FILE, 'r') as f:
        juegos = json.load(f)

    total_bombeo = 0
    total_produccion = 0
    total_peso = 0

    for juego in juegos:
        if not juego:
            continue

        valores_iniciales = juego[0].get("valores_iniciales")
        valores_finales = juego[-1].get("valores_finales")

        if not valores_iniciales or not valores_finales:
            continue

        eficacia = evaluar_eficacia(valores_iniciales, valores_finales)
        peso = max(0.1, eficacia + 1)  # evitar peso cero o negativo

        # Promediar las decisiones intermedias ponderadas por el score del juego
        for ronda in juego[1:-1]:
            decision = ronda.get("decision")
            if not decision:
                continue

            total_bombeo += decision.get("fraccion_bombeo", 0.5) * peso
            total_produccion += decision.get("produccion_planeada", 900) * peso

        total_peso += peso * (len(juego) - 2)  # solo rondas intermedias aportan decisiones

    if total_peso == 0:
        print("No se pudieron ajustar parámetros por falta de datos efectivos.")
        return

    nuevos_parametros = {
        "fraccion_bombeo_base": round(total_bombeo / total_peso, 3),
        "produccion_planeada_base": round(total_produccion / total_peso)
    }

    guardar_parametros(nuevos_parametros)
    print("🔄 Parámetros ajustados:", nuevos_parametros)
