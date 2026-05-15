from core.config import SYSTEM_PROMPT
from core.data_loader import load_metadata
from core.llm import create_llm
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from typing import List, Dict
from core.schemas import AnalysisPlan


def convert_st_chat_history(st_chat_history: List[Dict]) -> List[Dict]:
    messages = []
    for msg in messages:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            messages.append(AIMessage(content=msg["content"]))

    return messages

def select_columns(llm, user_query, metadata, st_chat_history):
    chat_history = convert_st_chat_history(st_chat_history)

    schema = AnalysisPlan.model_json_schema()

    messages = [
        SystemMessage(content= f"""
           {SYSTEM_PROMPT}

            Metadata:
            {metadata}
        """),
        *chat_history,
        HumanMessage(content=user_query)
        
    ]

    response = llm.invoke(messages)

    return response.content


if __name__ == "__main__":
   
    llm = create_llm()
    metadata = load_metadata()

    USER_QUERY = "what is the average ckt score for the different ages?"
    response = select_columns(llm, USER_QUERY, metadata)
    print(response)
