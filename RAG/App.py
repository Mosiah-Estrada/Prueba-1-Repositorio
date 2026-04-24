import streamlit as st
import os
from dotenv import load_dotenv
from Codigo import agent_executor # Importa la lógica del agente
# Configuración visual de la página
st.set_page_config(page_title="HR-Bot TechSolutions", page_icon="🤖")
st.title("🤖 HR-Bot: TechSolutions Chile")
st.markdown("### Asistente Inteligente de Recursos Humanos")
st.info("Consulta sobre vacaciones, beneficios y reglamentos internos de forma inmediata.")

# Historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Interacción
if prompt := st.chat_input("¿Cuál es tu duda sobre RRHH?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Buscando en manuales oficiales..."):
            try:
                # El agente decide si usar RAG interno o herramienta externa (IE5)
                result = agent_executor.invoke({"input": prompt})
                response = result["output"]
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Error de conexión: {e}")