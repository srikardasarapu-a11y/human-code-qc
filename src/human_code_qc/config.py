import os
import yaml
from dotenv import load_dotenv

load_dotenv()

DATASET_PATH = os.getenv("DATASET_PATH")
LITELLM_BASE_URL = os.getenv("LITELLM_BASE_URL", "http://localhost:4000")
LITELLM_MODEL = os.getenv("LITELLM_MODEL", "code-repair")
LITELLM_MASTER_KEY = os.getenv("LITELLM_MASTER_KEY")

def load_litellm_config():
    # Points to C:\Users\srika\OneDrive\Desktop\humancodeproject\human-code-qc\config\litellm.yaml
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "config", "litellm.yaml"))
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            return yaml.safe_load(f)
    return {}

LITELLM_CONFIG = load_litellm_config()
