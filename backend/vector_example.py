from langchain_community.chat_models import AzureChatOpenAI
from langchain_postgres import PGVector
from langchain_openai import AzureOpenAIEmbeddings
from langchain_core.documents import Document

OPENAI_API_KEY=""
# Updates azure embedding left is azure deployment 
embeddings = AzureOpenAIEmbeddings(
    model="text-embedding-ada-002",
    azure_endpoint="https://azurechat-aillm-rshepqjzo5msq.openai.azure.com/openai/deployments/embedding/embeddings?api-version=2023-05-15",
    api_key=OPENAI_API_KEY,
    openai_api_version="2023-05-15",
)

# See docker command above to launch a postgres instance with pgvector enabled.
connection = "postgresql+psycopg://postgres:admin@localhost:5432/sow"  # Uses psycopg3!
collection_name = "sow_embeddings"

vector_store = PGVector(
    embeddings=embeddings,
    collection_name=collection_name,
    connection=connection,
    use_jsonb=True,
)

docs = [
        Document(    
            page_content="""
                content goes here
            """,
            metadata={"id": 1, "fileName": "TEXAS_DIR_SOW"},
        ),
    ]


vector_store.add_documents(docs, ids=[doc.metadata["id"] for doc in docs])