# Lógica Mental – Motor en Python para el *Food Production Game*

> Código asociado a la tesis investigativa **“Comparación de recomendaciones en toma de decisiones dinámicas: Lógica mental vs. modelos de lenguaje (LLM)”**, realizada por estudiantes de la **Universidad de Talca (Chile)**.  
> Autores: **Benjamín Soto González** y **Carlos Tomás Rodríguez Rodríguez**.

Este repositorio contiene un motor basado en **lógica mental con memoria de corto y largo plazo** que genera recomendaciones en el entorno del simulador **Food Production Game**. Incluye una interfaz en **Streamlit** (`main.py`) para facilitar su ejecución y exploración por lectores y revisores.

---

## Tabla de contenidos
- [Descripción](#descripción)
- [Arquitectura del proyecto](#arquitectura-del-proyecto)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Ejecución](#ejecución)
- [Datos de ejemplo](#datos-de-ejemplo)
- [Pruebas rápidas](#pruebas-rápidas)
- [Reproducibilidad y versión de la tesis](#reproducibilidad-y-versión-de-la-tesis)
- [Cómo citar](#cómo-citar)
- [Licencia](#licencia)
- [Autores y afiliación](#autores-y-afiliación)

---

## Descripción
Este software implementa un **sistema de reglas (lógica mental)** que compara el estado actual con experiencias pasadas para proponer decisiones (p. ej., consumo/bombeo de agua y producción), considerando **memoria de corto y largo plazo**. Está diseñado para ejecutarse junto a un simulador de decisiones dinámicas (Food Production Game) y fue desarrollado como parte de una **tesis investigativa**.

> **Propósito académico**: El código se publica con fines de transparencia, replicabilidad y revisión por pares. No está orientado a uso productivo sin la debida validación.

---

## Arquitectura del proyecto
```text
food-production-mental-logic/
├─ main.py                         # Interfaz Streamlit (UI)
├─ motor_logico.py                 # Reglas y recomendaciones
├─ memoria.py                      # Persistencia: corto/largo plazo
├─ ajustar_parametros.py           # Rutinas de ajuste de parámetros
├─ visualizar_evolucion.py         # Gráficas/visualización de resultados (si aplica)
├─ experiencias_actual.json        # Memoria de corto plazo (ejemplo/fixture)
├─ experiencias_historial.json     # Memoria de largo plazo (ejemplo/fixture)
├─ parametros_ajustados.json       # Parámetros de calibración (ejemplo)
├─ requirements.txt                # Dependencias mínimas
├─ CITATION.cff                    # Metadatos de citación académica
├─ LICENSE                         # Licencia del proyecto (MIT por defecto)
└─ README.md                       # Este documento
```

---

## Requisitos
- **Python** 3.10, 3.11 o 3.12 (recomendado 3.11)
- **Sistemas operativos**: Windows, macOS o Linux
- **Bibliotecas necesarias** (se instalan con `requirements.txt`):
  - `streamlit` – interfaz web para ejecutar `main.py`
  - `pandas` – manejo de datos tabulares
  - `numpy` – operaciones numéricas
  - `matplotlib` – visualización simple

---

## Instalación
1. **Clonar** el repositorio
   ```bash
   git clone https://github.com/onlyzaetta/food-production-mental-logic.git
   cd food-production-mental-logic
   ```
2. **Crear** y **activar** un entorno virtual
   ```bash
   # Windows (PowerShell)
   python -m venv .venv
   .venv\Scripts\Activate.ps1

   # macOS/Linux (bash/zsh)
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

---

## Ejecución
### Interfaz (Streamlit)
Ejecuta la aplicación desde la raíz del proyecto:
```bash
streamlit run main.py
```
Luego abre el enlace local que aparezca en la terminal (por lo general `http://localhost:8501`).

---

## Datos de ejemplo
Incluye (opcionalmente) archivos **anonimizados** en la raíz (`experiencias_*.json`) o en una carpeta `experiencias/` para permitir una prueba rápida. Evita subir datos sensibles o licenciados.

---

## Pruebas rápidas
- Ejecuta un flujo mínimo con parámetros ficticios para verificar que `motor_logico.py` y `memoria.py` interactúan correctamente.
- (Opcional) Agrega pruebas unitarias con `pytest` y un workflow sencillo en GitHub Actions.

---

## Reproducibilidad y versión de la tesis
Para enlazar desde el libro, usa una **etiqueta inmutable**:
```bash
git tag -a v1.2.0 -m "Versión asociada a la tesis (28 Oct 2025)"
git push --tags
```

---

## Cómo citar
Este repositorio incluye un archivo `CITATION.cff` para que GitHub muestre “Cite this repository”. Ejemplo de cita 

- Soto González, B., & Rodríguez Rodríguez, C. T. (2025). *Lógica Mental – Motor en Python para el Food Production Game* (v1.2.0) [Software]. GitHub. https://github.com/onlyzaetta/food-production-mental-logic/tree/v1.2.0

**BibTeX**
```bibtex
@software{logica_mental_2025,
  author    = {Benjamín Soto González and Carlos Tomás Rodríguez Rodríguez},
  title     = {L{\'o}gica Mental -- Motor en Python para el Food Production Game},
  version   = {v1.2.0},
  year      = {2025},
  publisher = {GitHub},
  url       = {https://github.com/onlyzaetta/food-production-mental-logic/tree/v1.2.0},
  note      = {Tesis investigativa de la Universidad de Talca (Chile)}
}
```

---

## Licencia
Este proyecto se distribuye bajo la licencia **MIT**. Consulta el archivo [`LICENSE`](./LICENSE) para más detalles.

---

## Autores y afiliación
- **Benjamín Soto González** — Autor, desarrollo, análisis y documentación.
- **Carlos Tomás Rodríguez Rodríguez** — Autor, desarrollo, análisis y documentación.

**Afiliación:** Universidad de Talca, Chile.

Para dudas o sugerencias, abre un *issue*.
