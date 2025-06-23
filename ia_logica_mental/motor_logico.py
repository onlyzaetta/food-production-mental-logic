from memoria import MemoriaDeCasos
import json
from pathlib import Path

class MotorLogico:
    def __init__(self):
        self.resultado = {}
        self.memoria = MemoriaDeCasos()
        self.experiencias_recientes = self.memoria.obtener_ultimas_rondas()
        self.parametros = self._cargar_parametros_aprendidos()

    def _cargar_parametros_aprendidos(self):
        ruta = Path("parametros_aprendidos.json")
        if ruta.exists():
            with open(ruta, "r") as f:
                return json.load(f)
        return {
            "fraccion_bombeo_base": 0.5,
            "produccion_planeada_base": 900
        }

    def procesar_estado(self, estado: dict) -> dict:
        # Partimos desde parámetros base aprendidos
        fr_base = self.parametros["fraccion_bombeo_base"]
        prod_base = self.parametros["produccion_planeada_base"]

        self.resultado = {
            "fraccion_bombeo": fr_base,
            "produccion_planeada": prod_base
        }

        if self.experiencias_recientes:
            anterior = self.experiencias_recientes[-1]["entrada"]

            # Comparar sustentabilidad
            sust_actual = estado["indice_sustentabilidad"]
            sust_prev = anterior.get("indice_sustentabilidad")
            if sust_prev and sust_prev > 0:
                delta_sust = (sust_prev - sust_actual) / sust_prev
                if delta_sust >= 0.10:
                    print("📉 Sustentabilidad bajó más de un 10%")
                    self.resultado["fraccion_bombeo"] = max(fr_base - 0.1, 0.1)
                    self.resultado["produccion_planeada"] = max(prod_base - 300, 100)

            # Comparar índice de ganancias
            gan_actual = estado["indice_ganancias"]
            gan_prev = anterior.get("indice_ganancias")
            if gan_prev and gan_prev > 0:
                delta_gan = (gan_prev - gan_actual) / gan_prev
                if delta_gan >= 0.10:
                    print("💸 Ganancias bajaron más de un 10%")
                    self.resultado["fraccion_bombeo"] = min(fr_base + 0.1, 1.0)
                    self.resultado["produccion_planeada"] = min(prod_base + 200, 2000)

            # Comparar agua superficial
            agua_actual = estado["agua_superficie"]
            agua_prev = anterior.get("agua_superficie")
            if agua_prev and agua_prev > 0:
                delta_agua = (agua_prev - agua_actual) / agua_prev
                if delta_agua >= 0.15:
                    print("🚱 Agua superficial bajó más de un 15%")
                    self.resultado["fraccion_bombeo"] = max(fr_base - 0.2, 0.1)
                    self.resultado["produccion_planeada"] = max(prod_base - 400, 100)

            # Comparar consumo real
            consumo_actual = estado["consumo_real"]
            consumo_prev = anterior.get("consumo_real")
            if consumo_prev and consumo_prev > 0:
                delta_consumo = (consumo_actual - consumo_prev) / consumo_prev
                if delta_consumo >= 0.10 and sust_actual < 0.7:
                    print("💧 Consumo aumentó >10% y baja sustentabilidad")
                    self.resultado["fraccion_bombeo"] = max(fr_base - 0.15, 0.1)
                    self.resultado["produccion_planeada"] = max(prod_base - 450, 100)

        # Guardar experiencia
        self.memoria.guardar_experiencia(
            entrada=estado,
            decision=self.resultado,
            resultado={}
        )

        return self.resultado
