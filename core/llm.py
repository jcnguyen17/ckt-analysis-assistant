from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

from core.config import (
    MODEL,
    MODEL_PROVIDER,
    TEMPERATURE
)

load_dotenv()

def create_llm():
    return init_chat_model(model=MODEL, model_provider=MODEL_PROVIDER, temperature=TEMPERATURE)


if __name__ == "__main__":
    llm = create_llm()
    response = llm.invoke("What model version are you")
    print(response.content)
