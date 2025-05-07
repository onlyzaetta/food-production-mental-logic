import json
from pathlib import Path

class MemoriaDeCasos:
    def __init__(self, archivo="experiencias.json"):
        self.archivo = Path(archivo)
        self.experiencias = self._cargar()

    def _cargar(self):
        if self.archivo.exists():
            with open(self.archivo, "r") as f:
                return json.load(f)
        return []

    def guardar_experiencia(self, entrada, decision, resultado):
        experiencia = {
            "entrada": entrada,
            "decision": decision,
            "resultado": resultado
        }
        self.experiencias.append(experiencia)
        self._guardar_archivo()

    def actualizar_ultima_experiencia_con_resultado(self, resultado):
        if self.experiencias:
            self.experiencias[-1]["resultado"] = resultado
            self._guardar_archivo()

    def _guardar_archivo(self):
        with open(self.archivo, "w") as f:
            json.dump(self.experiencias, f, indent=4)

    def obtener_todas(self):
        return self.experiencias

    def __len__(self):
        return len(self.experiencias)
