"""
Essa classe permite utilizarmos as variáveis de ambiente definidas no arquivo .env de forma estruturada e fácil de acessar.
Assim evitamos a necessidade de acessar diretamente as variáveis de ambiente em todo o código.
"""

import os
from dotenv import load_dotenv


class Settings:
    load_dotenv()
    DATABRICKS_HOST = os.getenv("DATABRICKS_HOST")
    DATABRICKS_TOKEN = os.getenv("DATABRICKS_TOKEN")

    MLFLOW_URI = os.getenv("MLFLOW_TRACKING_URI", "databricks")
    EXPERIMENT_ID = os.getenv("EXPERIMENT_ID")

    VS_ENDPOINT = os.getenv("VS_ENDPOINT")
    INDEX_NAME = os.getenv("INDEX_NAME")
    LLM_ENDPOINT = os.getenv("LLM_ENDPOINT")
    MODEL_NAME = os.getenv("MODEL_NAME")
    DATABRICKS_HTTP_PATH = os.getenv("DATABRICKS_HTTP_PATH")


settings = Settings()
