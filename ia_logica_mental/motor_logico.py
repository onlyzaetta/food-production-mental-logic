from experta import Fact, KnowledgeEngine, Rule, P

# Hecho personalizado para describir el estado del simulador
class Estado(Fact):
    """Hechos que representan el estado actual del entorno"""
    pass

# Motor lógico basado en reglas tipo lógica mental
class MotorLogico(KnowledgeEngine):

    def __init__(self):
        super().__init__()
        self.resultado = {}

    @Rule(Estado(agua_subterranea=P(lambda a: a < 0.4), sostenibilidad=P(lambda s: s > 0.6)))
    def esquema_1_demandar_bombeo_moderado(self):
        print("🧠 Esquema activado: agua baja + sostenibilidad alta")
        self.resultado["fraccion_bombeo"] = 0.60
        self.resultado["produccion_planeada"] = 800

    @Rule(Estado(precipitaciones=P(lambda p: p > 80), ganancias=P(lambda g: g > 3000)))
    def esquema_2_aprovechar_buen_contexto(self):
        print("🧠 Esquema activado: condiciones favorables para aumentar")
        self.resultado["fraccion_bombeo"] = 0.75
        self.resultado["produccion_planeada"] = 1200

    @Rule(Estado(sostenibilidad=P(lambda s: s < 0.3), ganancias=P(lambda g: g < 1000)))
    def esquema_3_reducir_para_proteger(self):
        print("🧠 Esquema activado: baja sostenibilidad y baja ganancia")
        self.resultado["fraccion_bombeo"] = 0.30
        self.resultado["produccion_planeada"] = 500

    @Rule(Estado(produccion=P(lambda p: p > 1200), sostenibilidad=P(lambda s: s < 0.4)))
    def esquema_4_produccion_excesiva_peligrosa(self):
        print("🧠 Esquema activado: producción muy alta y sostenibilidad baja")
        self.resultado["fraccion_bombeo"] = 0.45
        self.resultado["produccion_planeada"] = 800

    @Rule(Estado(sostenibilidad=P(lambda s: s > 0.85), ganancias=P(lambda g: g > 4000)))
    def esquema_5_mantener_optimo(self):
        print("🧠 Esquema activado: buen equilibrio económico y ecológico")
        self.resultado["fraccion_bombeo"] = 0.50
        self.resultado["produccion_planeada"] = 1000
