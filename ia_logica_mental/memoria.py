import json
from pathlib import Path
from typing import List, Dict
from copy import deepcopy

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
            json.dump(data, f, indent=4, ensure_ascii=False)

    # -------- UTILIDAD: normalizar y copiar estructuras --------
    def _normalizar_decision(self, decision: Dict) -> Dict:
        d = decision or {}
        return {
            "fraccion_bombeo": d.get("fraccion_bombeo"),
            "produccion_planeada": d.get("produccion_planeada"),
            "condiciones_aplicadas": list(d.get("condiciones_aplicadas", [])),
            "razon_recomendacion": list(d.get("razon_recomendacion", [])),
        }

    # ------------------ MÉTODOS CLAVE ------------------
    def guardar_experiencia(self, entrada: dict, decision: dict, resultado: dict):
        """
        Convención:
        - Se llama al inicio de cada ronda con 'entrada' (estado observado al inicio),
          y la 'decision' calculada para ESA ronda.
        - El 'resultado' de la ronda previa se completa cuando llega la 'entrada' de la ronda actual.
        - En la ronda 10, 'entrada' se guarda como 'resultado' de la ronda 10 (no crear ronda 11).
        """
        ronda_n = len(self.experiencias_actual)
        entrada_cp = deepcopy(entrada)
        decision_norm = self._normalizar_decision(deepcopy(decision))

        if ronda_n == 0:
            # 1ª ronda: valores iniciales + decisión vacía o presente (según el flujo)
            experiencia = {
                "valores_iniciales": entrada_cp,
                "decision": decision_norm,
                "condiciones_aplicadas": list(decision_norm.get("condiciones_aplicadas", [])),
                "resultado": {}
            }
            self.experiencias_actual.append(experiencia)

        elif ronda_n < 10:
            # Rondas intermedias: agrego la DECISIÓN de la ronda actual
            experiencia = {
                "decision": decision_norm,
                "condiciones_aplicadas": list(decision_norm.get("condiciones_aplicadas", [])),
                "resultado": {}
            }
            self.experiencias_actual.append(experiencia)

            # Y relleno el RESULTADO de la ronda anterior con la 'entrada' actual
            # (la anterior es -2 porque recién añadimos la actual al final)
            self.experiencias_actual[-2]["resultado"] = entrada_cp

        elif ronda_n == 10:
            # Ya hay 10 elementos: la 'entrada' actual corresponde al RESULTADO de la ronda 10
            # y archivamos; no se crea una 11ª entrada.
            self.experiencias_actual[-1]["resultado"] = entrada_cp
            self._guardar(self.archivo_actual, self.experiencias_actual)
            self._archivar_juego()
            return

        self._guardar(self.archivo_actual, self.experiencias_actual)

    def actualizar_ultima_experiencia_con_resultado(self, resultado: dict):
        if self.experiencias_actual:
            self.experiencias_actual[-1]["resultado"] = deepcopy(resultado)
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
