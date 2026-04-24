# HR-Bot TechSolutions Chile - Pipeline RAG

Este proyecto implementa un asistente virtual de Recursos Humanos utilizando **LangChain** y **GPT-4o** para resolver dudas frecuentes de los colaboradores basadas en manuales internos.

## Estructura del Proyecto
- `.env`: Variables de entorno (Tokens y URLs).
- `RAG/app.py`: Interfaz de usuario desarrollada en Streamlit.
- `RAG/Codigo.py`: Lógica del agente, embeddings y motor de búsqueda vectorial.
- `RAG/data/`: Carpeta que contiene el `manual_empleado.pdf`.

## Requisitos
- Python 3.10
- Librerías: `streamlit`, `langchain`, `langchain-openai`, `faiss-cpu`, `python-dotenv`, `pypdf`.

## Instrucciones de Ejecución
1. Configurar el archivo `.env` con el `GITHUB_TOKEN`.
2. Asegurar que el manual PDF esté en la carpeta `data`.
3. Ejecutar el siguiente comando desde la terminal:
   ```bash
   cd RAG
   python -m streamlit run App.py