from pathlib import Path
from core.schemas import AnalysisPlan
BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------
# Paths
# ------------------
PROJECT_PATH = "ckt"
METADATA_PATH = BASE_DIR / PROJECT_PATH /"metadata.yaml"

# Data location
# TODO: makes this dynamic
DATA_DIR = BASE_DIR / "data" / "input"


# ------------------
# Chat model configuration
# ------------------

# ChatGPT
#MODEL_PROVIDER = "openai"
#MODEL = "gpt-5.2"
#TEMPERATURE = 0

MODEL_PROVIDER = "ollama"
#MODEL = "qwen3:1.7b"
#MODEL = "gemma3:4b"
MODEL = "deepseek-r1:14b"
TEMPERATURE = 0


# system prompt
# For each different project

#----- CKT Analysis assistant
SYSTEM_PROMPT = f"""
    You are an AI assistant that maps user analysis questions to the correct dataset

    You job is to convert the user's natural language question into a structured JSON analysis plan
   
    You do not:
        - calculate the results
        - create charts
    
    Use the supplied metadata to choose:
        - the dataset
        - the analysis type
        - variables
        - filters
        - group_by columns
        - aggregation
    
    Only use what is supplied in the metadata.

    For categorical fulters, return the exact value from metadata allowed_values.

    If the request is ambigious or cannot be mapped safely, set clarification_required and provide a clarification_question


    Rules for response:
    Return JSON matching this schema
    {AnalysisPlan.model_json_schema()}

"""


if __name__ == "__main__":
    print(f"METADATA_PATH {METADATA_PATH}")
    print(f"DATA_DIR {DATA_DIR}")