"""
Criando toda a estrutura do "backend" da aplicação.
Aqui definimos a lógica de RAG, o retriever, o prompt e a chain completa.
"""

from databricks_langchain import ChatDatabricks, DatabricksVectorSearch
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda, RunnableMap
from langchain_core.output_parsers import StrOutputParser
from settings import settings
import mlflow.langchain
from typing import List, Any


def get_retriever() -> Any:
    """Retorna o retriever configurado para busca vetorial."""
    return DatabricksVectorSearch(
        endpoint=settings.VS_ENDPOINT,
        index_name=settings.INDEX_NAME,
        columns=["material_name", "description", "ton", "price"],
    ).as_retriever(search_kwargs={"k": 5, "query_type": "hybrid"})


def format_context(docs: List[Any]) -> str:
    """Formata os documentos recuperados para o prompt."""
    if not docs:
        return ""
    return "\n\nContexto adicional:\n" + "\n".join(
        f"- Nome: {getattr(doc, 'metadata', {}).get('material_name', 'N/A')}\n"
        f"  Descrição: {getattr(doc, 'page_content', doc.metadata.get('description', 'Descrição não disponível'))}\n"
        f"  Quantidade em estoque (ton): {getattr(doc, 'metadata', {}).get('ton', 'não informada')}"
        for doc in docs
    )


def get_prompt() -> PromptTemplate:
    """Lê o template do prompt de um arquivo externo."""
    with open("prompt_template.txt", encoding="utf-8") as f:
        template = f.read()
    return PromptTemplate.from_template(template)


def ensure_query_format(query: dict) -> str:
    """Garante que a query do usuário seja string."""
    return query.get("messages", "") or query.get("query", "")


def get_rag_chain() -> Any:
    """Inicializa e retorna a chain RAG completa, retornando sempre texto livre da LLM."""
    retriever = get_retriever()
    prompt = get_prompt()
    llm = ChatDatabricks(endpoint=settings.LLM_ENDPOINT)

    rag_chain = (
        RunnableMap(
            {
                "query": RunnableLambda(lambda x: ensure_query_format(x)),
                "context": RunnableLambda(lambda x: ensure_query_format(x))
                | retriever
                | RunnableLambda(format_context),
            }
        )
        | prompt
        | llm
        | StrOutputParser()
    )
    mlflow.set_tracking_uri(settings.MLFLOW_URI)
    mlflow.set_experiment(settings.EXPERIMENT_ID)
    mlflow.langchain.autolog()
    return rag_chain
