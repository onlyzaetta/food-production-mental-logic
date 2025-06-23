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
            with open(archivo, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def _guardar(self, archivo: Path, data):
        with open(archivo, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def guardar_experiencia(self, entrada: dict, decision: dict, resultado: dict):
        ronda_n = len(self.experiencias_actual)

        if ronda_n == 0:
            # Primera ronda: guardar como valores iniciales y decisión
            experiencia = {
                "valores_iniciales": entrada,
                "decision": decision,
                "resultado": {}
            }
        elif ronda_n == 10:
            # Ronda final: entrada se guarda como resultado final
            self.experiencias_actual.append({
                "valores_finales": entrada,
                "decision": {},  # no hay recomendación en esta ronda
                "resultado": {}
            })
            self._guardar(self.archivo_actual, self.experiencias_actual)
            self._archivar_juego()
            return
        else:
            # Rondas intermedias: guardar decisión y resultado (resultado se rellena al siguiente ciclo)
            experiencia = {
                "decision": decision,
                "resultado": {}  # se rellena en la siguiente ronda
            }

        self.experiencias_actual.append(experiencia)
        self._guardar(self.archivo_actual, self.experiencias_actual)

        # A partir de la segunda ronda, rellenamos el resultado de la anterior
        if ronda_n >= 1:
            self.experiencias_actual[-2]["resultado"] = entrada
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

            # Ajustar los parámetros después de guardar un juego completo
            from ajustar_parametros import ajustar_parametros
            ajustar_parametros()
