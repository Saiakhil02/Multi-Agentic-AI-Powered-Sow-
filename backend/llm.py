from langchain_community.chat_models import AzureChatOpenAI

# from langchain_core.messages import HumanMessage, SystemMessage
from config import OPENAI_API_KEY, AZURE_DEPLOYMENT_NAME, AZURE_MODEL_NAME, AZURE_API_BASE_URL

if not (OPENAI_API_KEY or AZURE_DEPLOYMENT_NAME or AZURE_MODEL_NAME or AZURE_API_BASE_URL) :
    raise ValueError("🚨 Environment variable not set! look for .env.example file.")

model = AzureChatOpenAI(
    model=AZURE_MODEL_NAME,
    deployment_name=AZURE_DEPLOYMENT_NAME,
    openai_api_key=OPENAI_API_KEY,
    openai_api_base=AZURE_API_BASE_URL,
    # Do not update this values unless Azure API changes it.
    # This is the default value for Azure OpenAI API and Not Model.
    openai_api_version="2023-05-15",
)
