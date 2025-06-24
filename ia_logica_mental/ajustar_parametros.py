import json
from pathlib import Path

PARAMS_FILE = Path("parametros_aprendidos.json")
HISTORIAL_FILE = Path("experiencias_historial.json")

def get_parametros_default():
    return {
        "reduccion_por_sustentabilidad": {
            "fraccion_bombeo": 0.35,
            "produccion_planeada": 600
        },
        "reduccion_por_ganancia": {
            "fraccion_bombeo": 0.40,
            "produccion_planeada": 700
        },
        "ajuste_por_agua_superficie_baja": {
            "fraccion_bombeo": 0.30,
            "produccion_planeada": 500
        },
        "sobreconsumo_con_sustentabilidad_baja": {
            "fraccion_bombeo": 0.25,
            "produccion_planeada": 450
        },
        "neutral": {
            "fraccion_bombeo": 0.50,
            "produccion_planeada": 900
        }
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

    categorias = {
        "reduccion_por_sustentabilidad": [],
        "reduccion_por_ganancia": [],
        "ajuste_por_agua_superficie_baja": [],
        "sobreconsumo_con_sustentabilidad_baja": [],
        "neutral": []
    }

    for juego in juegos:
        if not juego:
            continue

        valores_iniciales = juego[0].get("valores_iniciales")
        valores_finales = juego[-1].get("valores_finales")

        if not valores_iniciales or not valores_finales:
            continue

        eficacia = evaluar_eficacia(valores_iniciales, valores_finales)
        peso = max(0.1, eficacia + 1)

        for ronda in juego[1:-1]:
            decision = ronda.get("decision")
            resultado = ronda.get("resultado")
            if not decision or not resultado:
                continue

            sust_actual = resultado.get("indice_sustentabilidad")
            sust_prev = valores_iniciales.get("indice_sustentabilidad")
            gan_actual = resultado.get("indice_ganancias")
            gan_prev = valores_iniciales.get("indice_ganancias")
            agua_actual = resultado.get("agua_superficie")
            agua_prev = valores_iniciales.get("agua_superficie")
            consumo_actual = resultado.get("consumo_real")
            consumo_prev = valores_iniciales.get("consumo_real")

            if sust_prev and sust_actual is not None and (sust_prev - sust_actual) / sust_prev >= 0.10:
                categorias["reduccion_por_sustentabilidad"].append((decision, peso))
            elif gan_prev and gan_actual is not None and (gan_prev - gan_actual) / gan_prev >= 0.10:
                categorias["reduccion_por_ganancia"].append((decision, peso))
            elif agua_prev and agua_actual is not None and (agua_prev - agua_actual) / agua_prev >= 0.15:
                categorias["ajuste_por_agua_superficie_baja"].append((decision, peso))
            elif consumo_prev and consumo_actual is not None and (consumo_actual - consumo_prev) / consumo_prev >= 0.10 and sust_actual < 0.7:
                categorias["sobreconsumo_con_sustentabilidad_baja"].append((decision, peso))
            else:
                categorias["neutral"].append((decision, peso))

    nuevos_parametros = {}
    for key, decisiones in categorias.items():
        if not decisiones:
            nuevos_parametros[key] = get_parametros_default()[key]
            continue

        total_bombeo = sum(d["fraccion_bombeo"] * p for d, p in decisiones)
        total_produccion = sum(d["produccion_planeada"] * p for d, p in decisiones)
        total_peso = sum(p for _, p in decisiones)

        nuevos_parametros[key] = {
            "fraccion_bombeo": round(total_bombeo / total_peso, 3),
            "produccion_planeada": round(total_produccion / total_peso)
        }

    guardar_parametros(nuevos_parametros)
    print("🔄 Parámetros ajustados:", nuevos_parametros)
