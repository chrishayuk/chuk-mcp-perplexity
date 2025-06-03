"""Unit-tests for the Perplexity MCP tools."""
from typing import Any, Dict, List

import pytest

from chuk_mcp_perplexity.tools import (
    perplexity_search,
    perplexity_deep_research,
)

# --------------------------------------------------------------------------- #
# Global monkey-patch for chuk-llm client
# --------------------------------------------------------------------------- #
@pytest.fixture(autouse=True)
def _patch_llm_client(monkeypatch):
    """Stub out get_llm_client everywhere so tests never touch the network."""

    class FakeClient:
        async def create_completion(self, messages: List[Dict[str, Any]], **_kw):
            return {"response": f"mock-answer: {messages[-1]['content']}"}

    def _fake_get_llm_client(*_args, **_kwargs):  # accepts any signature
        return FakeClient()

    # Patch the canonical location…
    import chuk_llm.llm.llm_client as llm_mod
    monkeypatch.setattr(llm_mod, "get_llm_client", _fake_get_llm_client)

    # …and the copy imported inside our tools module.
    import chuk_mcp_perplexity.tools as tools_mod
    monkeypatch.setattr(tools_mod, "get_llm_client", _fake_get_llm_client)

    yield


# --------------------------------------------------------------------------- #
# Success paths
# --------------------------------------------------------------------------- #
@pytest.mark.asyncio
async def test_search_success():
    result = await perplexity_search("Hello?")
    assert result == {"answer": "mock-answer: Hello?"}


@pytest.mark.asyncio
async def test_deep_research_success():
    question = "Explain GPT-4o in 3 sentences."
    result = await perplexity_deep_research(question)
    assert result == {"answer": f"mock-answer: {question}"}


# --------------------------------------------------------------------------- #
# Validation errors
# --------------------------------------------------------------------------- #
@pytest.mark.asyncio
@pytest.mark.parametrize("func", [perplexity_search, perplexity_deep_research])
async def test_validation_error(func):
    with pytest.raises(ValueError):
        await func(123)  # type: ignore[arg-type]
