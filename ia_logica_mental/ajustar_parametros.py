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
        "reduccion_por_sobre_consumo": 100,
        "aumento_por_bajas_precipitaciones": 100,
        "reduccion_por_bajas_reservas": 100,
        "aumento_por_altas_ganancias": 100
    }

def cargar_parametros():
    if PARAMS_FILE.exists():
        with open(PARAMS_FILE, 'r') as f:
            return json.load(f)
    return get_parametros_default()

def guardar_parametros(parametros):
    with open(PARAMS_FILE, 'w') as f:
        json.dump(parametros, f, indent=4)

def ajustar_parametros():
    if not HISTORIAL_FILE.exists():
        print(" No hay historial para ajustar parámetros.")
        return

    with open(HISTORIAL_FILE, 'r', encoding='utf-8') as f:
        juegos = json.load(f)

    acumuladores = {clave: [] for clave in get_parametros_default()}

    for juego in juegos:
        if not juego or len(juego) < 3:
            continue

        for i in range(2, len(juego)-1):
            actual = juego[i]
            anterior = juego[i-1]

            condiciones = actual.get("condiciones_aplicadas", [])
            resultado_actual = actual.get("resultado", {})
            resultado_anterior = anterior.get("resultado", {})

            gan_ant = resultado_anterior.get("indice_ganancias")
            sust_ant = resultado_anterior.get("indice_sustentabilidad")
            prod_ant = resultado_anterior.get("produccion_real")
            
            gan_act = resultado_actual.get("indice_ganancias")
            sust_act = resultado_actual.get("indice_sustentabilidad")
            prod_act = resultado_actual.get("produccion_real")

            if None in [gan_act, gan_ant, sust_act, sust_ant, prod_act, prod_ant]:
                continue

            cambio_en_ganancias = gan_act - gan_ant
            cambio_en_sustentabilidad = sust_act - sust_ant
            cambio_en_produccion = prod_act - prod_ant

            for condicion in condiciones:
                if condicion not in acumuladores:
                    continue

                # Evaluación de impacto de cada parametro en los indicadores
                
                # Si la produccion y las ganancias ahumentaron y la sustentabilidad no bajó demaciado
                if cambio_en_produccion > 0 and cambio_en_ganancias > 0 and cambio_en_sustentabilidad > -10:
                    acumuladores[condicion].append(1)
                # Si la produccion o la sustentabilidad bajan   
                elif cambio_en_produccion < 0 or cambio_en_sustentabilidad < 0:
                    acumuladores[condicion].append(-1)
                # neutro
                else:
                    acumuladores[condicion].append(0)

    # Cargar parámetros actuales
    parametros = cargar_parametros()

    # Ajuste según evaluación de impacto
    for clave, impactos in acumuladores.items():
        if not impactos:
            continue

        promedio = sum(impactos) / len(impactos)
        ajuste = promedio * 10  # impacto ajusta en ±10 unidades
        nuevo_valor = parametros.get(clave, 100) + ajuste
        parametros[clave] = max(10, round(nuevo_valor))  # límite mínimo

    guardar_parametros(parametros)
    print(" Parámetros ajustados:", parametros)
