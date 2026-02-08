# app.py
import streamlit as st
from main import get_rag_chain, ensure_query_format
import mlflow
import os
import json

st.title("🏗️ Assistente Comercial de Materiais Industriais")
st.caption(
    "Recomenda materiais com base na aplicação do cliente usando RAG + Vector Search"
)

st.set_page_config(page_title="🤖 Assistente Comercial de Materiais", layout="centered")


# Inicialização da Chain (cacheada)


@st.cache_resource
def initialize_chain():
    """Inicializa a chain RAG apenas uma vez."""
    return get_rag_chain()


chain = initialize_chain()

# Histórico de Chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Olá! 👋\n\n"
                "Descreva a **aplicação do material** que o cliente precisa "
                "(ex: suspensão de ônibus, estrutura metálica, torres de transmissão)."
            ),
        }
    ]

# Exibir histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Entrada do Usuário
if user_query := st.chat_input("Descreva a necessidade do cliente..."):
    # Salva mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": user_query})

    with st.chat_message("user"):
        st.write(user_query)

    # Processamento RAG
    with st.chat_message("assistant"):
        with st.spinner("🔍 Buscando materiais mais adequados..."):
            with mlflow.start_run(run_name="material_rag_chat") as run:
                # Invoca a chain com a query do usuário, garantindo o formato correto
                input_data = {"messages": user_query}
                response = chain.invoke(input_data)

                # Log básico no MLflow
                mlflow.log_param("consulta_usuario", user_query)
                mlflow.log_param("run_id", run.info.run_id)

                # Tratamento da Resposta (JSON)

                st.subheader("📌 Resposta do Assistente")
                st.write(response)
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": response,
                    }
                )

# Sidebar – Informações Técnicas
with st.sidebar:
    st.header("⚙️ Configurações Técnicas")
    st.write(f"**LLM Endpoint:** `{os.getenv('LLM_ENDPOINT')}`")
    st.write(f"**Vector Search Endpoint:** `{os.getenv('VS_ENDPOINT')}`")
    st.write(f"**Índice:** `{os.getenv('INDEX_NAME')}`")
    st.markdown("---")
    st.caption(
        "O agente utiliza RAG com foco na descrição de uso dos materiais "
        "para apoiar o time comercial."
    )
