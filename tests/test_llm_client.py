import pytest
from src.human_code_qc.llm.client import LLMRepairEngine

def test_llm_repair_disabled_by_default():
    engine = LLMRepairEngine(enable_repair=False)
    original_code = "print('hello')"
    meta = {}
    
    repaired, changed = engine.attempt_repair(original_code, meta, ["error"])
    
    assert repaired == original_code
    assert changed is False
