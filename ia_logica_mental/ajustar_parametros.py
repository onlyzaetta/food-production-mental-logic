import json
from pathlib import Path

PARAMS_FILE = Path("parametros_ajustados.json")
HISTORIAL_FILE = Path("experiencias_historial.json")


def get_parametros_default():
    return {
        "reduccion_por_capacidad_produccion": 100,
        "reduccion_por_capacidad_consumo": 100,
        "aumento_por_bajo_indice_ganancia": 100,
        "reduccion_por_bajo_indice_susten": 100,
        "reduccion_por_sobre_consumo": 100
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
        "reduccion_por_capacidad_produccion": [],
        "reduccion_por_capacidad_consumo": [],
        "aumento_por_bajo_indice_ganancia": [],
        "reduccion_por_bajo_indice_susten": [],
        "reduccion_por_sobre_consumo": []
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

            prod_plan = resultado.get("produccion_planeada")
            prod_real = resultado.get("produccion_real")
            consumo_plan = resultado.get("consumo_planeado")
            consumo_real = resultado.get("consumo_real")
            gan_prev = valores_iniciales.get("indice_ganancias")
            gan_actual = resultado.get("indice_ganancias")
            sust_prev = valores_iniciales.get("indice_sustentabilidad")
            sust_actual = resultado.get("indice_sustentabilidad")
            agua_prev = valores_iniciales.get("agua_superficie")
            agua_actual = resultado.get("agua_superficie")

            if prod_plan is not None and prod_real is not None and (prod_plan - prod_real) > 0:
                categorias["reduccion_por_capacidad_produccion"].append((100, peso))
            if consumo_plan is not None and consumo_real is not None and (consumo_plan - consumo_real) > 0:
                categorias["reduccion_por_capacidad_consumo"].append((100, peso))
            if gan_prev is not None and gan_actual is not None and (gan_prev - gan_actual) > 5:
                categorias["aumento_por_bajo_indice_ganancia"].append((100, peso))
            if sust_prev is not None and sust_actual is not None and (sust_prev - sust_actual) > 5:
                categorias["reduccion_por_bajo_indice_susten"].append((100, peso))
            if agua_prev is not None and agua_actual is not None and (agua_prev - agua_actual) > (0.15 * agua_prev):
                categorias["reduccion_por_sobre_consumo"].append((100, peso))

    nuevos_parametros = {}
    for key, ajustes in categorias.items():
        if not ajustes:
            nuevos_parametros[key] = get_parametros_default()[key]
            continue

        total_ponderado = sum(valor * peso for valor, peso in ajustes)
        total_pesos = sum(peso for _, peso in ajustes)
        nuevos_parametros[key] = round(total_ponderado / total_pesos)

    guardar_parametros(nuevos_parametros)
    print("🔄 Parámetros ajustados:", nuevos_parametros)
