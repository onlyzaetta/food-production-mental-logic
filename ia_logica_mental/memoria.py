import json
from pathlib import Path
from typing import List, Dict

class MemoriaDeCasos:
    def __init__(self, archivo_actual="experiencias_actual.json", archivo_historial="experiencias_historial.json"):
        self.archivo_actual = Path(archivo_actual)
        self.archivo_historial = Path(archivo_historial)

        self.experiencias_actual: List[Dict] = self._cargar(self.archivo_actual)
        self.experiencias_historial: List[List[Dict]] = self._cargar(self.archivo_historial)

    def _cargar(self, archivo: Path):
        if archivo.exists():
            if archivo.stat().st_size == 0:
                return []
            with open(archivo, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def _guardar(self, archivo: Path, data):
        with open(archivo, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def guardar_experiencia(self, entrada: dict, decision: dict, resultado: dict):
        ronda_n = len(self.experiencias_actual)
        condiciones = decision.get("condiciones_aplicadas", [])

        if ronda_n == 0:
            experiencia = {
                "valores_iniciales": entrada,
                "decision": decision,
                "condiciones_aplicadas": condiciones,
                "resultado": {}
            }
            self.experiencias_actual.append(experiencia)

        elif ronda_n < 10:
            experiencia = {
                "decision": decision,
                "condiciones_aplicadas": condiciones,
                "resultado": {}
            }
            self.experiencias_actual.append(experiencia)
            self.experiencias_actual[-2]["resultado"] = entrada  # Guardar resultado de ronda anterior

        elif ronda_n == 10:
            # Guardar como resultado de la última ronda real
            self.experiencias_actual[-1]["resultado"] = entrada
            self._guardar(self.archivo_actual, self.experiencias_actual)
            self._archivar_juego()
            return

        self._guardar(self.archivo_actual, self.experiencias_actual)



    def actualizar_ultima_experiencia_con_resultado(self, resultado: dict):
        if self.experiencias_actual:
            self.experiencias_actual[-1]["resultado"] = resultado
            self._guardar(self.archivo_actual, self.experiencias_actual)

    def obtener_ultimas_rondas(self, n=10):
        return self.experiencias_actual[-n:]

    def _archivar_juego(self):
        if self.experiencias_actual:
            self.experiencias_historial.append(self.experiencias_actual)
            self._guardar(self.archivo_historial, self.experiencias_historial)
            self.experiencias_actual = []
            self._guardar(self.archivo_actual, self.experiencias_actual)

            from ajustar_parametros import ajustar_parametros
            ajustar_parametros()
