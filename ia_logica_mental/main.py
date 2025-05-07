import streamlit as st
from motor_logico import Estado, MotorLogico
from memoria import MemoriaDeCasos

st.title("Simulador de decisiones - Lógica Mental")

st.subheader("Estado actual del entorno")

agua_superficie = st.number_input("Agua en superficie (m³)", min_value=0.0, max_value=7000.0)
precipitaciones = st.number_input("Precipitaciones anuales (m³/año)", min_value=0.0, max_value=10000.0)
produccion_real = st.number_input("Producción real (kg/año)", min_value=0.0, max_value=2000.0)
ganancias = st.number_input("Ganancias acumuladas ($ miles)", min_value=0.0)
sustentabilidad = st.number_input("Índice de sustentabilidad (0 a 1)", min_value=0.0, max_value=1.0, step=0.01)

if st.button("Enviar a IA basada en lógica mental"):
    estado = {
        "agua_superficie": agua_superficie,
        "precipitaciones": precipitaciones,
        "produccion_real": produccion_real,
        "ganancias": ganancias,
        "sustentabilidad": sustentabilidad
    }

    st.success("Estado registrado. Procesando con lógica mental...")

    # Actualizar resultado de la ronda anterior
    memoria = MemoriaDeCasos()
    memoria.actualizar_ultima_experiencia_con_resultado(estado)

    # Iniciar motor de inferencia
    motor = MotorLogico()
    motor.reset()

    motor.declare(Estado(
        agua_superficie=estado["agua_superficie"],
        precipitaciones=estado["precipitaciones"],
        produccion=estado["produccion_real"],
        ganancias=estado["ganancias"],
        sustentabilidad=estado["sustentabilidad"]
    ))

    motor.run()

    # Mostrar resultado
    if motor.resultado:
        st.subheader("💡 Recomendación:")
        fraccion = motor.resultado.get("fraccion_bombeo", "No definida")
        produccion = motor.resultado.get("produccion_planeada", "No definida")
        consumo_agua = produccion * 5 if isinstance(produccion, (int, float)) else "-"
        st.write(f"Fracción de bombeo recomendada: {fraccion}")
        st.write(f"Producción planeada recomendada: {produccion} kg/año")
        st.write(f"Consumo estimado de agua: {consumo_agua} m³/año")
    else:
        st.info("No se activó ninguna regla. Considera agregar más reglas al motor lógico.")

    # Guardar experiencia (sin resultado, que se completará en la siguiente ronda)
    memoria.guardar_experiencia(
        entrada=estado,
        decision=motor.resultado,
        resultado={}  # se actualiza en la siguiente ejecución
    )
    st.success("📁 Experiencia registrada para futuras comparaciones.")
