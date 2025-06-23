from experta import Fact, KnowledgeEngine, Rule, P
from memoria import MemoriaDeCasos

# Hecho personalizado para describir el estado del simulador
class Estado(Fact):
    """Hechos que representan el estado actual del entorno"""
    pass

class MotorLogico(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.resultado = {}
        self.memoria = MemoriaDeCasos()
        self.experiencias_recientes = self.memoria.obtener_ultimas_rondas()

    def procesar_estado(self, estado: dict) -> dict:
        self.reset()

        # Guardar valores para acceder dentro de reglas si se requiere
        self.estado_actual = estado
        self.experiencias_recientes = self.memoria.obtener_ultimas_rondas()

        # Declarar hechos para el motor
        self.declare(Estado(
            agua_superficie=estado["agua_superficie"],
            produccion_planeada=estado["produccion_planeada"],
            produccion_real=estado["produccion_real"],
            consumo_planeado=estado["consumo_planeado"],
            consumo_real=estado["consumo_real"],
            indice_ganancias=estado["indice_ganancias"],
            indice_sustentabilidad=estado["indice_sustentabilidad"]
        ))

        self.run()

        # Guardar experiencia en memoria (sin resultado, se actualizaría después si se deseara)
        self.memoria.guardar_experiencia(entrada=estado, decision=self.resultado, resultado={})

        return self.resultado

    # --- Reglas de procesamiento ---

    @Rule(Estado(indice_sustentabilidad=P(lambda s: s < 0.4), indice_ganancias=P(lambda g: g < 0.4)))
    def baja_sustentabilidad_bajas_ganancias(self):
        print("⚠️ Sustentabilidad y ganancias bajas, reducir producción")
        self.resultado["fraccion_bombeo"] = 0.30
        self.resultado["produccion_planeada"] = 500

    @Rule(Estado(agua_superficie=P(lambda a: a < 2000)))
    def escasez_agua_superficial(self):
        print("🚱 Agua superficial muy baja")
        self.resultado["fraccion_bombeo"] = 0.40
        self.resultado["produccion_planeada"] = 600

    @Rule(Estado(consumo_real=P(lambda c: c > 7000), indice_sustentabilidad=P(lambda s: s < 0.5)))
    def sobreconsumo_contra_sustentabilidad(self):
        print("💧 Consumo alto y sustentabilidad baja")
        self.resultado["fraccion_bombeo"] = 0.35
        self.resultado["produccion_planeada"] = 500

    @Rule(Estado(indice_sustentabilidad=P(lambda s: s > 0.8), indice_ganancias=P(lambda g: g > 0.7)))
    def equilibrio_ideal(self):
        print("✅ Buen equilibrio, mantener niveles actuales")
        self.resultado["fraccion_bombeo"] = 0.55
        self.resultado["produccion_planeada"] = 1000
