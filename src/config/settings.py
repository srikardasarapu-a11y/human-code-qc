# Placeholder config settings
import os
import yaml

def load_litellm_config():
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "config", "litellm.yaml"))
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            return yaml.safe_load(f)
    return {}
