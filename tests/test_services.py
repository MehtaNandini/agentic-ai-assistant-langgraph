import os
import pytest
from unittest.mock import patch
from app.services.llm import get_llm

@patch.dict(os.environ, {"GROQ_API_KEY": "dummy_key"})
def test_get_llm_success():
    llm = get_llm()
    assert llm is not None
    assert getattr(llm, "model_name", None) == "llama-3.1-8b-instant" or getattr(llm, "model", None) == "llama-3.1-8b-instant"

@patch.dict(os.environ, {}, clear=True)
def test_get_llm_missing_api_key():
    with pytest.raises(ValueError, match="GROQ_API_KEY environment variable is missing"):
        get_llm()
