#Instalacion de dependencias#

#pip install streamlit
#pip install langchain
#pip install langchain-openai
#pip install langchain-community
#pip install faiss-cpu
#pip install pypdf
#pip install python-dotenv
#pip install tiktoken

################################

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.tools.retriever import create_retriever_tool
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain import hub

load_dotenv()  # Carga variables de entorno desde .env

# Configuración de modelos (IE5: Arquitectura)
llm = ChatOpenAI(
    base_url=os.environ.get("OPENAI_BASE_URL"),
    api_key=os.environ.get("GITHUB_TOKEN"),
    model="gpt-4o",
    temperature=0
)

embeddings = OpenAIEmbeddings(
    base_url=os.environ.get("OPENAI_EMBEDDINGS_URL"),
    api_key=os.environ.get("GITHUB_TOKEN"),
    model="text-embedding-3-small"
)

# Pipeline RAG y Configuración de Chunks (IE3, IE4)
def inicializar_agente_rrhh():
    loader = PyPDFLoader("data/manual_empleado.pdf")
    docs = loader.load()
    
    # Fragmentación para precisión (1000 caracteres con 150 de solapamiento)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = text_splitter.split_documents(docs)
    
    vectorstore = FAISS.from_documents(chunks, embeddings)
    retriever = vectorstore.as_retriever()

    # Herramienta de consulta interna
    tool_rag = create_retriever_tool(
        retriever,
        "manual_techsolutions",
        "Consulta este manual para dudas sobre beneficios y políticas. Cita siempre la página."
    )

    # Prompt optimizado (IE2) con reglas de Privacidad y Trazabilidad
    instrucciones = """Eres el HR-Bot de TechSolutions Chile.
    - TRAZABILIDAD: Indica siempre el documento y sección (ej. 'Según Manual de Beneficios, pág 4').
    - PRIVACIDAD: No des información sobre sueldos o datos personales.
    - Si la información no está en los manuales, responde que no tienes ese registro."""

    prompt = hub.pull("hwchase17/openai-functions-agent")
    prompt.messages[0].prompt.template = instrucciones

    agent = create_openai_functions_agent(llm, [tool_rag], prompt)
    return AgentExecutor(agent=agent, tools=[tool_rag], verbose=True)

agent_executor = inicializar_agente_rrhh()