import os
from src.human_code_qc.config import LITELLM_CONFIG, LITELLM_MODEL, LITELLM_BASE_URL

def test_config_loaded():
    assert isinstance(LITELLM_CONFIG, dict)
    
def test_env_variables_have_defaults():
    assert LITELLM_MODEL is not None
    assert LITELLM_BASE_URL is not None
