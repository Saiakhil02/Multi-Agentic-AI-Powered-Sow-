import os
from dotenv import load_dotenv, find_dotenv
# Load environment variables from the .env file
load_dotenv(find_dotenv())


OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_DEPLOYMENT_NAME = os.getenv("AZURE_DEPLOYMENT_NAME")
AZURE_MODEL_NAME = os.getenv("AZURE_MODEL_NAME")
AZURE_API_BASE_URL = os.getenv("AZURE_API_BASE_URL")
AZURE_TEXT_EMBEDDING = os.getenv("AZURE_TEXT_EMBEDDING")
AZURE_EMBEDDING_URL_PATH = os.getenv("AZURE_EMBEDDING_URL_PATH")
POSTGRESQL_BASE_URL= os.getenv("POSTGRESQL_BASE_URL")
EMBEDDING_COL_NAME= os.getenv("EMBEDDING_COL_NAME")