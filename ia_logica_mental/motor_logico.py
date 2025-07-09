from memoria import MemoriaDeCasos
import json
from pathlib import Path

class MotorLogico:

    def __init__(self):
        self.resultado = {}
        self.memoria = MemoriaDeCasos()
        self.experiencias_recientes = self.memoria.obtener_ultimas_rondas()
        self.parametros = self._cargar_parametros_aprendidos()
        self.recomendacionBombeo = 500
        self.recomendacionProduccion = 1000

    def _cargar_parametros_aprendidos(self):
        ruta = Path("parametros_ajustados.json")
        if ruta.exists():
            with open(ruta, "r") as f:
                return json.load(f)
        return {
            "reduccion_produccion_por_capacidad_produccion": 100,
            "reduccion_produccion_por_capacidad_consumo": 100,
            "aumento_por_bajo_indice_ganancia": 100,
            "reduccion_por_bajo_indice_susten": 100,
            "reduccion_por_sobre_consumo": 100
        }

    def procesar_estado(self, estado: dict) -> dict:
        condiciones_aplicadas = []

        # Valores base
        self.recomendacionBombeo = 500
        self.recomendacionProduccion = 1000

        if self.experiencias_recientes:
            anterior = self.experiencias_recientes[-1].get("valores_iniciales") or \
                       self.experiencias_recientes[-1].get("resultado")

            prod_plan_actual = estado.get("produccion_planeada")
            prod_real_actual = estado.get("produccion_real")
            sust_actual = estado.get("indice_sustentabilidad")
            sust_prev = anterior.get("indice_sustentabilidad")
            gan_actual = estado.get("indice_ganancias")
            gan_prev = anterior.get("indice_ganancias")
            agua_actual = estado.get("agua_superficie")
            agua_prev = anterior.get("agua_superficie")
            consumo_agua_planeado = estado.get("consumo_planeado")
            consumo_agua_real = estado.get("consumo_real")

            # -producción planeada (PP) - producción real (PR) > 0
            if prod_plan_actual is not None and prod_real_actual is not None and (prod_plan_actual - prod_real_actual > 0):
                self.recomendacionProduccion -= self.parametros["reduccion_produccion_por_capacidad_produccion"]
                condiciones_aplicadas.append("reduccion_por_capacidad_produccion")
            # -consumo planeado (CP) - consumo real (CR) > 0
            if consumo_agua_planeado is not None and consumo_agua_real is not None and (consumo_agua_planeado - consumo_agua_real > 0):
                self.recomendacionProduccion -= self.parametros["reduccion_produccion_por_capacidad_consumo"]
                condiciones_aplicadas.append("reduccion_por_capacidad_consumo")
            # -índice de ganancias disminuye más de un 5%
            if gan_prev is not None and gan_actual is not None and (gan_prev - gan_actual > 5):
                self.recomendacionBombeo += self.parametros["aumento_por_bajo_indice_ganancia"]
                self.recomendacionProduccion += self.parametros["aumento_por_bajo_indice_ganancia"] * 5
                condiciones_aplicadas.append("aumento_por_bajo_indice_ganancia")
            # -índice de sustentabilidad disminuye más de un 5%
            if sust_prev is not None and sust_actual is not None and (sust_prev - sust_actual > 5):
                self.recomendacionBombeo -= self.parametros["reduccion_por_bajo_indice_susten"]
                self.recomendacionProduccion -= self.parametros["reduccion_por_bajo_indice_susten"] * 5
                condiciones_aplicadas.append("reduccion_por_bajo_indice_susten")
            # -Agua en superficie disminuye más de un 15%
            if agua_prev is not None and agua_actual is not None and (agua_prev - agua_actual > 0.15 * agua_prev):
                self.recomendacionBombeo -= self.parametros["reduccion_por_sobre_consumo"]
                condiciones_aplicadas.append("reduccion_por_sobre_consumo")

        # Resultado final de la ronda
        self.resultado = {
            "fraccion_bombeo": self.recomendacionBombeo,
            "produccion_planeada": self.recomendacionProduccion,
            "condiciones_aplicadas": condiciones_aplicadas
        }

        # Guardar experiencia con condiciones
        self.memoria.guardar_experiencia(
            entrada=estado,
            decision=self.resultado,
            resultado={}
        )

        return self.resultado
