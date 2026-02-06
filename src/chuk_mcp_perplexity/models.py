"""chuk_mcp_perplexity.models

Pydantic models used by the Perplexity MCP tools.
"""

from pydantic import BaseModel, Field


# ───────────────────────── Search (sonar-pro) ──────────────────────────
class PerplexitySearchInput(BaseModel):
    """Input payload for the *perplexity_search* tool."""

    query: str = Field(..., description="User query to be answered briefly")


class PerplexitySearchResult(BaseModel):
    """Return payload for the *perplexity_search* tool."""

    answer: str = Field(..., description="Short conversational answer")


# ───────────────────── Deep-research (sonar-deep-research) ─────────────
class PerplexityResearchInput(BaseModel):
    """Input payload for the *perplexity_deep_research* tool."""

    query: str = Field(..., description="User query requiring in-depth research")


class PerplexityResearchResult(BaseModel):
    """Return payload for the *perplexity_deep_research* tool."""

    answer: str = Field(..., description="Comprehensive, citation-rich answer")
