import yaml
from core.config import METADATA_PATH

def load_metadata() -> dict:
    with open(METADATA_PATH, "r", encoding="utf-8") as file:
        metadata = yaml.safe_load(file)
    
    return metadata