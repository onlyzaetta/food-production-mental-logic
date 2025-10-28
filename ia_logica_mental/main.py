import streamlit as st
from motor_logico import MotorLogico

st.title("Simulador de decisiones - Lógica Mental")

st.subheader("Estado actual del entorno")

# Inputs definidos
# Agua y consumo
agua_superficie = st.number_input("Agua en superficie (m³)", min_value=0, max_value=7000)
precipitaciones = st.number_input(" Precipitaciones", min_value=2000, max_value=7000)
reservas = st.number_input("Total estimado de reservas", min_value=1000, max_value=360000, step=1000)
consumo_planeado = st.number_input("Consumo planeado", min_value=0, max_value=9000)
consumo_real = st.number_input("Consumo real", min_value=0, max_value=9000)
bombeo_planeado= st.number_input("Bombeo planeado", min_value=0,max_value=10000)
bombeo_real = st.number_input("Bombeo real", min_value=0, max_value=10000)
#Produccion y ganancias
produccion_planeada = st.number_input("Producción planeada", min_value=0, max_value=2000)
produccion_real = st.number_input("Producción real (kg/año)", min_value=0, max_value=2000)
produccion_acumulada = st.number_input("Produccion acumulada", min_value=0, max_value=100000, step=100)
ganancias_anuales = st.number_input("Ganancias anuales", min_value=0, max_value=9000, step=10)
ganancias_acumuladas = st.number_input("Ganancias acumuladas", min_value=0, max_value=450000, step=1)
#Indices
indice_ganancias = st.number_input("Índice de ganancias", min_value=0, max_value=100, step=1)
indice_sustentabilidad = st.number_input("Índice de sustentabilidad", min_value=0, max_value=100, step=1)
indice_rendimiento = st.number_input("Índice de rendimiento", min_value=0, max_value=100, step=1)

if st.button("Enviar a motor lógico"):

    estado = {
        "agua_superficie": agua_superficie,
        "precipitaciones": precipitaciones,
        "reservas": reservas,
        "consumo_planeado": consumo_planeado,
        "consumo_real": consumo_real,
        "bombeo_planeado": bombeo_planeado,
        "bombeo_real": bombeo_real,
        "produccion_planeada": produccion_planeada,
        "produccion_real": produccion_real,
        "produccion_acumulada": produccion_acumulada,
        "ganancias_anuales": ganancias_anuales,
        "ganancias_acumuladas": ganancias_acumuladas,
        "indice_ganancias": indice_ganancias,
        "indice_sustentabilidad": indice_sustentabilidad,
        "indice_rendimiento": indice_rendimiento
    }

    st.success(" Estado recibido. Procesando recomendación...")

    motor = MotorLogico()
    resultado = motor.procesar_estado(estado)


    if "mensaje" in resultado:
        st.info(f"ℹ {resultado['mensaje']}")
    else:
        st.subheader(" Recomendación:")
        st.write(f"Fracción de bombeo recomendada: {resultado.get('fraccion_bombeo', 'No definida')} %")
        st.write(f"Producción planeada recomendada: {resultado.get('produccion_planeada', 'No definida')} kg/año")

        if isinstance(resultado.get("produccion_planeada"), (int, float)):
            consumo_estimado = resultado["produccion_planeada"] * 5
            st.write(f"Consumo estimado de agua: {consumo_estimado} m³/año")
        else:
            st.write("Consumo estimado de agua: -")

        condiciones = resultado.get("razon_recomendacion", [])
        if condiciones:
            st.markdown("### Razón(es) de la recomendación:")
            for condicion in condiciones:
                st.write(f"• {condicion}")



if st.button(" Visualizar evolución de parámetros y resultados"):
    import visualizar_evolucion
    visualizar_evolucion.mostrar_graficos()
