"""chuk_mcp_perplexity.tools

Async MCP tools backed by Perplexity Sonar models via **chuk-llm**
with per-tool timeout configuration
=================================================================

Exposed tools
-------------
* **perplexity_search** - quick answers with `sonar-pro` (30s timeout).
* **perplexity_deep_research** - long-form research answers with
  `sonar-deep-research` (90s timeout).

Key points
~~~~~~~~~~
* The tools are **native async** with configurable per-tool timeouts
* Each tool has an appropriate timeout based on expected response time
* Timeout can be overridden in config.yaml or environment variables
"""

from __future__ import annotations

from typing import Dict, List

from pydantic import ValidationError

from chuk_llm.llm.llm_client import get_llm_client
from chuk_mcp_runtime.common.mcp_tool_decorator import mcp_tool

from .models import (
    PerplexitySearchInput,
    PerplexitySearchResult,
    PerplexityResearchInput,
    PerplexityResearchResult,
)

# ---------------------------------------------------------------------------
# Tool: perplexity_search (30 second timeout)
# ---------------------------------------------------------------------------
@mcp_tool(
    name="perplexity_search",
    description="Quick conversational answer using Perplexity sonar-pro",
    timeout=30  # 30 seconds for quick search
)
async def perplexity_search(query: str) -> Dict:
    """
    Return a short, conversational answer using Perplexity sonar-pro.
    
    Args:
        query: User query to be answered briefly
    """
    try:
        validated = PerplexitySearchInput(query=query)
    except ValidationError as exc:
        raise ValueError(f"Invalid input for perplexity_search: {exc}")

    client = get_llm_client("perplexity", model="sonar-pro")
    messages: List[Dict[str, str]] = [
        {"role": "user", "content": validated.query}
    ]
    result = await client.create_completion(messages)
    return PerplexitySearchResult(answer=result["response"]).model_dump()


# ---------------------------------------------------------------------------
# Tool: perplexity_deep_research (90 second timeout)
# ---------------------------------------------------------------------------
@mcp_tool(
    name="perplexity_deep_research",
    description="Comprehensive, citation-rich answer using Perplexity sonar-deep-research",
    timeout=90  # 90 seconds for deep research
)
async def perplexity_deep_research(query: str) -> Dict:
    """
    Return an in-depth, well-sourced answer using Perplexity sonar-deep-research.
    
    Args:
        query: User query requiring in-depth research
    """
    try:
        validated = PerplexityResearchInput(query=query)
    except ValidationError as exc:
        raise ValueError(f"Invalid input for perplexity_deep_research: {exc}")

    client = get_llm_client("perplexity", model="sonar-deep-research")
    messages = [{"role": "user", "content": validated.query}]
    result = await client.create_completion(messages)
    return PerplexityResearchResult(answer=result["response"]).model_dump()


# ---------------------------------------------------------------------------
# Tool: perplexity_quick_fact (15 second timeout)
# ---------------------------------------------------------------------------
@mcp_tool(
    name="perplexity_quick_fact",
    description="Ultra-fast fact checking using Perplexity sonar-pro",
    timeout=15  # 15 seconds for quick facts
)
async def perplexity_quick_fact(query: str) -> Dict:
    """
    Return a quick factual answer for simple queries.
    
    Args:
        query: Simple factual query
    """
    try:
        validated = PerplexitySearchInput(query=f"Quick fact: {query}")
    except ValidationError as exc:
        raise ValueError(f"Invalid input for perplexity_quick_fact: {exc}")

    client = get_llm_client("perplexity", model="sonar-pro")
    messages = [{"role": "user", "content": validated.query}]
    result = await client.create_completion(messages)
    return PerplexitySearchResult(answer=result["response"]).model_dump()