from config import OPENAI_API_KEY, AZURE_DEPLOYMENT_NAME, AZURE_MODEL_NAME, AZURE_API_BASE_URL, AZURE_TEXT_EMBEDDING, AZURE_EMBEDDING_URL_PATH, POSTGRESQL_BASE_URL, EMBEDDING_COL_NAME
from langchain_postgres import PGVector
from langchain_openai import AzureOpenAIEmbeddings

# embedding from where to use 
embeddings = AzureOpenAIEmbeddings(
    model=AZURE_TEXT_EMBEDDING,
    azure_endpoint=f"{AZURE_API_BASE_URL}{AZURE_EMBEDDING_URL_PATH}",
    api_key=OPENAI_API_KEY,
    openai_api_version="2023-05-15",
)

vector_store = PGVector(
    embeddings=embeddings,
    collection_name=EMBEDDING_COL_NAME,
    connection= f"postgresql+psycopg://{POSTGRESQL_BASE_URL}",
    use_jsonb=True,
)

# Quering embeddings 
retriever = vector_store.as_retriever(search_type="mmr", search_kwargs={"k": 2})