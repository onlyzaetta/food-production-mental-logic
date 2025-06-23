import json
from pathlib import Path

class MemoriaDeCasos:
    def __init__(self, archivo_actual="experiencias_actual.json", archivo_historial="experiencias_historial.json"):
        self.archivo_actual = Path(archivo_actual)
        self.archivo_historial = Path(archivo_historial)

        self.experiencias_actual = self._cargar(self.archivo_actual)
        self.experiencias_historial = self._cargar(self.archivo_historial)

    def _cargar(self, archivo):
        if archivo.exists():
            with open(archivo, "r") as f:
                return json.load(f)
        return []

    def _guardar(self, archivo, data):
        with open(archivo, "w") as f:
            json.dump(data, f, indent=4)

    def guardar_experiencia(self, entrada, decision, resultado):
        experiencia = {
            "entrada": entrada,
            "decision": decision,
            "resultado": resultado
        }

        self.experiencias_actual.append(experiencia)

        if len(self.experiencias_actual) >= 10:
            self.archivar_juego_actual()
        else:
            self._guardar(self.archivo_actual, self.experiencias_actual)

    def actualizar_ultima_experiencia_con_resultado(self, resultado):
        if self.experiencias_actual:
            self.experiencias_actual[-1]["resultado"] = resultado
            self._guardar(self.archivo_actual, self.experiencias_actual)

    def obtener_ultimas_rondas(self, n=10):
        return self.experiencias_actual[-n:]

    def archivar_juego_actual(self):
        """Mover las 10 rondas a memoria de largo plazo y limpiar la memoria actual"""
        if len(self.experiencias_actual) >= 10:
            self.experiencias_historial.append(self.experiencias_actual[:10])
            self._guardar(self.archivo_historial, self.experiencias_historial)

            self.experiencias_actual = []
            self._guardar(self.archivo_actual, self.experiencias_actual)
            print("📦 Juego archivado en historial y memoria actual limpiada.")
