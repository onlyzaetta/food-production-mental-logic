import streamlit as st
from motor_logico import MotorLogico

st.title("Simulador de decisiones - Lógica Mental")

st.subheader("Estado actual del entorno")

# Inputs definidos
agua_superficie = st.number_input("Agua en superficie (m³)", min_value=0.0, max_value=7000.0)
produccion_planeada = st.number_input("Producción planeada", min_value=0.0, max_value=2000.0)
produccion_real = st.number_input("Producción real (kg/año)", min_value=0.0, max_value=2000.0)
consumo_planeado = st.number_input("Consumo planeado", min_value=0.0, max_value=9000.0)
consumo_real = st.number_input("Consumo real", min_value=0.0, max_value=9000.0)
indice_ganancias = st.number_input("Índice de ganancias", min_value=0.0, max_value=1.0, step=0.01)
indice_sustentabilidad = st.number_input("Índice de sustentabilidad", min_value=0.0, max_value=1.0, step=0.01)

if st.button("Enviar a IA basada en lógica mental"):

    # Armar el estado como diccionario simple
    estado = {
        "agua_superficie": agua_superficie,
        "consumo_planeado": consumo_planeado,
        "consumo_real": consumo_real,
        "produccion_planeada": produccion_planeada,
        "produccion_real": produccion_real,
        "indice_ganancias": indice_ganancias,
        "indice_sustentabilidad": indice_sustentabilidad
    }

    st.success("✅ Estado recibido. Procesando recomendación...")

    # Procesar con motor lógico
    motor = MotorLogico()
    resultado = motor.procesar_estado(estado)

    # Mostrar resultado
    st.subheader("💡 Recomendación:")
    st.write(f"Fracción de bombeo recomendada: {resultado.get('fraccion_bombeo', 'No definida')}")
    st.write(f"Producción planeada recomendada: {resultado.get('produccion_planeada', 'No definida')} kg/año")
    if isinstance(resultado.get("produccion_planeada"), (int, float)):
        consumo_estimado = resultado["produccion_planeada"] * 5
        st.write(f"Consumo estimado de agua: {consumo_estimado} m³/año")
    else:
        st.write("Consumo estimado de agua: -")

        
    if st.button("📊 Visualizar evolución de parámetros y resultados"):
        import visualizar_evolucion
        visualizar_evolucion.mostrar_graficos()
