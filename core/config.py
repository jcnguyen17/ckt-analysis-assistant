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
DATA_FILE = BASE_DIR / "data" / "input" / "gold_student_exam_summary.csv"


# ------------------
# Chat model configuration
# ------------------

# ChatGPT
MODEL_PROVIDER = "openai"
MODEL = "gpt-5.2"
#TEMPERATURE = 0

#MODEL_PROVIDER = "ollama"
#MODEL = "qwen3:1.7b"
#MODEL = "gemma3:4b"
TEMPERATURE = 0


# system prompt
# For each different project

#----- CKT Analysis assistant
SYSTEM_PROMPT = f"""
    You are an AI assistant that maps user analysis questions to the correct dataset

    Your job is not to calculate the anaswer

    Your job is to identify:
    1. the metric column
    2. the aggregation
    3. the demographic / group by column

    Ask the user if you are unsure which exam they are referring to

    Rules for response:
    Return JSON matching this schema
    {AnalysisPlan.model_json_schema()}

    When applying filters to categorical columns you must return the exact stored dataframe value
    from allowed_values, not natural language
    
    Example:
    User says "show me female students vs ckt1 scores"
    Return:
    "value": "F"

"""


