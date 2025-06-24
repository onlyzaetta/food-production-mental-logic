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
            "reduccion_por_sustentabilidad": {"fraccion_bombeo": 0.35, "produccion_planeada": 600},
            "reduccion_por_ganancia": {"fraccion_bombeo": 0.4, "produccion_planeada": 700},
            "ajuste_por_agua_superficie_baja": {"fraccion_bombeo": 0.3, "produccion_planeada": 500},
            "sobreconsumo_con_sustentabilidad_baja": {"fraccion_bombeo": 0.25, "produccion_planeada": 450},
            "neutral": {"fraccion_bombeo": 0.5, "produccion_planeada": 900}
        }

    def procesar_estado(self, estado: dict) -> dict:
        # Por defecto, aplicar parámetros neutrales
        self.resultado = dict(self.parametros["neutral"])

        if self.experiencias_recientes:
            anterior = self.experiencias_recientes[-1]["entrada"]

            sust_actual = estado.get("indice_sustentabilidad")
            sust_prev = anterior.get("indice_sustentabilidad")
            gan_actual = estado.get("indice_ganancias")
            gan_prev = anterior.get("indice_ganancias")
            agua_actual = estado.get("agua_superficie")
            agua_prev = anterior.get("agua_superficie")
            consumo_actual = estado.get("consumo_real")
            consumo_prev = anterior.get("consumo_real")

            # Detectar situación y aplicar parámetros aprendidos
            if sust_prev and sust_prev > 0:
                delta_sust = (sust_prev - sust_actual) / sust_prev
                if delta_sust >= 0.10:
                    print("📉 Sustentabilidad bajó más de un 10%")
                    self.resultado = dict(self.parametros["reduccion_por_sustentabilidad"])

            if gan_prev and gan_prev > 0:
                delta_gan = (gan_prev - gan_actual) / gan_prev
                if delta_gan >= 0.10:
                    print("💸 Ganancias bajaron más de un 10%")
                    self.resultado = dict(self.parametros["reduccion_por_ganancia"])

            if agua_prev and agua_prev > 0:
                delta_agua = (agua_prev - agua_actual) / agua_prev
                if delta_agua >= 0.15:
                    print("🚱 Agua superficial bajó más de un 15%")
                    self.resultado = dict(self.parametros["ajuste_por_agua_superficie_baja"])

            if consumo_prev and consumo_prev > 0:
                delta_consumo = (consumo_actual - consumo_prev) / consumo_prev
                if delta_consumo >= 0.10 and sust_actual < 0.7:
                    print("💧 Consumo aumentó >10% y baja sustentabilidad")
                    self.resultado = dict(self.parametros["sobreconsumo_con_sustentabilidad_baja"])

        # Guardar experiencia
        self.memoria.guardar_experiencia(
            entrada=estado,
            decision=self.resultado,
            resultado={}
        )

        return self.resultado
