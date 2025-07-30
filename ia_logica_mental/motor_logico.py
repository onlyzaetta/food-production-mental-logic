from memoria import MemoriaDeCasos
import json
from pathlib import Path

class MotorLogico:

    def __init__(self):
        self.resultado = {}
        self.memoria = MemoriaDeCasos()
        self.experiencias_recientes = self.memoria.obtener_ultimas_rondas()
        self.parametros = self._cargar_parametros_aprendidos()
        #Valores de recomendacion base
        self.recomendacionBombeo = 50
        self.recomendacionProduccion = 500

    def _cargar_parametros_aprendidos(self):
        ruta = Path("parametros_ajustados.json")
        if ruta.exists():
            with open(ruta, "r") as f:
                return json.load(f)
        ## Valores por defecto en caso de fallo al buscar y leer archivo
        return {
            "reduccion_produccion_por_capacidad_produccion": 100,
            "reduccion_produccion_por_capacidad_consumo": 100,
            "aumento_por_bajo_indice_ganancia": 100,
            "reduccion_por_bajo_indice_susten": 100,
            "reduccion_por_sobre_consumo": 100,
            "aumento_por_bajas_precipitaciones": 100,
            "reduccion_por_bajas_reservas": 100,
            "aumento_por_altas_ganancias": 100
        }

    def procesar_estado(self, estado: dict) -> dict:
        condiciones_aplicadas = []
        razon_recomendacion = []

        # Si ya hay 10 rondas, solo se espera el resultado final
        if len(self.experiencias_recientes) == 10:
            self.memoria.guardar_experiencia(
                entrada=estado, decision={}, resultado={}
            )
            return {
                "mensaje": "La simulación ha sido almacenada en memoria para su análisis"
            }

        if self.experiencias_recientes:

            for experiencia in reversed(self.experiencias_recientes):
                anterior = experiencia.get("resultado") or experiencia.get("valores_iniciales")
                if anterior:  # Asegura que no esté vacío
                    break                       

            sust_prev = anterior.get("indice_sustentabilidad")
            gan_prev = anterior.get("indice_ganancias")
            agua_prev = anterior.get("agua_superficie")
            precipitaciones_prev = anterior.get("precipitaciones")            
            reservas_prev = anterior.get("reservas")
            gan_previas = anterior.get("ganancias_anuales")

            prod_plan_actual = estado.get("produccion_planeada")
            prod_real_actual = estado.get("produccion_real")
            sust_actual = estado.get("indice_sustentabilidad")
            gan_actual = estado.get("indice_ganancias")
            agua_actual = estado.get("agua_superficie")
            bombeo_agua_planeado = estado.get("bombeo_planeado")
            bombeo_agua_real = estado.get("bombeo_real")
            precipitaciones_actual = estado.get("precipitaciones")
            reservas_actual = estado.get("reservas")
            gan_actuales = estado.get("ganancias_anuales")


            self.recomendacionBombeo = 50
            self.recomendacionProduccion = 500

            # Si existe una recomendacion previa se utiliza para lo valores base
            if prod_plan_actual is not None and bombeo_agua_planeado is not None:
                self.recomendacionProduccion = prod_plan_actual
                self.recomendacionBombeo = bombeo_agua_planeado


            # -producción planeada (PP) - producción real (PR) > 0
            if (prod_plan_actual - prod_real_actual > 0) or (bombeo_agua_planeado - bombeo_agua_real > 0):
                self.recomendacionProduccion -= self.parametros["reduccion_por_capacidad_produccion"]
                condiciones_aplicadas.append("reduccion_por_capacidad_produccion")
                razon_recomendacion.append("Reducir la producción por que se sobrepasó la capacidad de produccion del terreno")
            
            # Antes de comparar con rondas previas aseguremonos de que no estén vacias
            if anterior:
                # -índice de ganancias disminuye más de un 3%
                if (gan_prev - gan_actual > 3):
                    self.recomendacionBombeo += self.parametros["aumento_por_bajo_indice_ganancia"] /10
                    self.recomendacionProduccion += self.parametros["aumento_por_bajo_indice_ganancia"]
                    condiciones_aplicadas.append("aumento_por_bajo_indice_ganancia")
                    razon_recomendacion.append("Aumento de la produccion y fraccion de bombeo debido a excesiva bajada del indice de produccion")
                # -índice de sustentabilidad disminuye más de un 3%
                if (sust_prev - sust_actual > 3):
                    self.recomendacionBombeo -= self.parametros["reduccion_por_bajo_indice_susten"] /10
                    self.recomendacionProduccion -= self.parametros["reduccion_por_bajo_indice_susten"]
                    condiciones_aplicadas.append("reduccion_por_bajo_indice_susten")
                    razon_recomendacion.append("Reducir la producción por bajada excesiva del índice de sustentabilidad")
                # -Agua en superficie disminuye más de un 10%
                if (agua_prev - agua_actual > 0.10 * agua_prev):
                    self.recomendacionBombeo -= self.parametros["reduccion_por_sobre_consumo"] /10
                    condiciones_aplicadas.append("reduccion_por_sobre_consumo")
                    razon_recomendacion.append("Reducir el bombeo debido al sobre consumo del agua en superficie")
                # Baja de precipitaciones mayor al 5%
                if precipitaciones_prev > 0 and (precipitaciones_prev - precipitaciones_actual) / precipitaciones_prev > 0.05:
                    self.recomendacionBombeo += self.parametros.get("aumento_por_bajas_precipitaciones", 100) / 10
                    condiciones_aplicadas.append("aumento_por_bajas_precipitaciones")
                    razon_recomendacion.append("Aumento de bombeo por baja significativa en precipitaciones")
                # Reservas bajan más de un 5%
                if reservas_prev > 0 and (reservas_prev - reservas_actual) / reservas_prev > 0.05:
                        self.recomendacionBombeo -= self.parametros.get("reduccion_por_bajas_reservas", 100) / 10
                        condiciones_aplicadas.append("reduccion_por_bajas_reservas")
                        razon_recomendacion.append("Reducción de bombeo por baja significativa en reservas disponibles")
                # Aumento de ganancias anuales mayor al 5%
                if gan_previas > 0 and (gan_actuales - gan_previas) / gan_previas > 0.05:
                        self.recomendacionProduccion += self.parametros.get("aumento_por_altas_ganancias", 100) / 10
                        condiciones_aplicadas.append("aumento_por_altas_ganancias")
                        razon_recomendacion.append("Aumento de producción debido a mejora significativa en ganancias anuales")

        
        # Normalizacion de bombeo y produccion para evitar que sobrepase el limite
        self.recomendacionBombeo = min(100, max(0, self.recomendacionBombeo))
        self.recomendacionProduccion = min(2000,max(0, self.recomendacionProduccion))

        # Resultado final de la ronda
        self.resultado = {
            "fraccion_bombeo": self.recomendacionBombeo,
            "produccion_planeada": self.recomendacionProduccion,
            "condiciones_aplicadas": condiciones_aplicadas,
            "razon_recomendacion": razon_recomendacion
        }

        # Guardar experiencia con condiciones
        self.memoria.guardar_experiencia(
            entrada=estado,
            decision=self.resultado,
            resultado={}
        )

        return self.resultado
