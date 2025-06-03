# debug_perplexity_tools.py
"""
Diagnostic script for debugging MCP Perplexity tools timeout issues.
"""
import asyncio
import logging
import time
from typing import Dict, List
from chuk_llm.llm.llm_client import get_llm_client

# Set up detailed logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

async def test_llm_client_direct():
    """Test the LLM client directly without MCP wrapper."""
    logger.info("Testing direct LLM client connection...")
    
    try:
        start_time = time.time()
        client = get_llm_client("perplexity", model="sonar-pro")
        logger.info(f"Client created in {time.time() - start_time:.2f}s")
        
        messages = [{"role": "user", "content": "What is 2+2?"}]
        
        # Test with timeout
        result = await asyncio.wait_for(
            client.create_completion(messages), 
            timeout=30.0
        )
        
        logger.info(f"Direct client test successful: {result}")
        return True
        
    except asyncio.TimeoutError:
        logger.error("Direct client test timed out after 30s")
        return False
    except Exception as e:
        logger.error(f"Direct client test failed: {e}")
        return False

async def test_perplexity_search_isolated():
    """Test the perplexity search function in isolation."""
    logger.info("Testing isolated perplexity_search function...")
    
    try:
        # Import your models
        from chuk_mcp_perplexity.models import PerplexitySearchInput, PerplexitySearchResult
        from pydantic import ValidationError
        
        query = "What is 2+2?"
        
        # Validate input
        validated = PerplexitySearchInput(query=query)
        logger.info(f"Input validation successful: {validated}")
        
        # Test client creation
        client = get_llm_client("perplexity", model="sonar-pro")
        logger.info("Client created successfully")
        
        # Test completion with timeout
        messages = [{"role": "user", "content": validated.query}]
        result = await asyncio.wait_for(
            client.create_completion(messages),
            timeout=30.0
        )
        
        # Wrap result
        final_result = PerplexitySearchResult(answer=result["response"])
        logger.info(f"Isolated test successful: {final_result}")
        return final_result.model_dump()
        
    except Exception as e:
        logger.error(f"Isolated test failed: {e}")
        return None

# Improved perplexity_search with better error handling and logging
async def improved_perplexity_search(query: str, timeout: float = 30.0) -> Dict:
    """
    Improved version of perplexity_search with better error handling and timeouts.
    
    Args:
        query: User query to be answered briefly
        timeout: Timeout in seconds for the operation
    """
    from chuk_mcp_perplexity.models import PerplexitySearchInput, PerplexitySearchResult
    from pydantic import ValidationError
    
    logger.info(f"Starting perplexity_search with query: {query}")
    start_time = time.time()
    
    try:
        # Validate input
        validated = PerplexitySearchInput(query=query)
        logger.debug(f"Input validated: {validated}")
        
        # Get client with error handling
        try:
            client = get_llm_client("perplexity", model="sonar-pro")
            logger.debug("LLM client created successfully")
        except Exception as e:
            logger.error(f"Failed to create LLM client: {e}")
            raise ValueError(f"LLM client initialization failed: {e}")
        
        # Prepare messages
        messages = [{"role": "user", "content": validated.query}]
        logger.debug(f"Messages prepared: {messages}")
        
        # Execute with timeout
        try:
            result = await asyncio.wait_for(
                client.create_completion(messages),
                timeout=timeout
            )
            logger.debug(f"LLM completion successful in {time.time() - start_time:.2f}s")
        except asyncio.TimeoutError:
            logger.error(f"LLM completion timed out after {timeout}s")
            raise TimeoutError(f"Perplexity search timed out after {timeout} seconds")
        except Exception as e:
            logger.error(f"LLM completion failed: {e}")
            raise RuntimeError(f"Perplexity search failed: {e}")
        
        # Validate result structure
        if not isinstance(result, dict) or "response" not in result:
            logger.error(f"Unexpected result structure: {result}")
            raise ValueError(f"Invalid response structure from LLM: {result}")
        
        # Create output
        output = PerplexitySearchResult(answer=result["response"])
        logger.info(f"perplexity_search completed successfully in {time.time() - start_time:.2f}s")
        
        return output.model_dump()
        
    except ValidationError as exc:
        logger.error(f"Input validation failed: {exc}")
        raise ValueError(f"Invalid input for perplexity_search: {exc}")
    except Exception as e:
        logger.error(f"perplexity_search failed after {time.time() - start_time:.2f}s: {e}")
        raise

# Updated tool registration with better error handling
from chuk_mcp_runtime.common.mcp_tool_decorator import mcp_tool

@mcp_tool(
    name="perplexity_search_improved",
    description="Quick conversational answer using Perplexity sonar-pro with improved error handling",
)
async def perplexity_search_improved(query: str) -> Dict:
    """
    Return a short, conversational answer with improved error handling.
    
    Args:
        query: User query to be answered briefly
    """
    return await improved_perplexity_search(query, timeout=30.0)

@mcp_tool(
    name="perplexity_deep_research_improved", 
    description="Comprehensive, citation-rich answer using Perplexity sonar-deep-research with improved error handling",
)
async def perplexity_deep_research_improved(query: str) -> Dict:
    """
    Return an in-depth, well-sourced answer with improved error handling.
    
    Args:
        query: User query requiring in-depth research
    """
    from chuk_mcp_perplexity.models import PerplexityResearchInput, PerplexityResearchResult
    from pydantic import ValidationError
    
    logger.info(f"Starting perplexity_deep_research with query: {query}")
    start_time = time.time()
    
    try:
        validated = PerplexityResearchInput(query=query)
        
        client = get_llm_client("perplexity", model="sonar-deep-research")
        messages = [{"role": "user", "content": validated.query}]
        
        # Use longer timeout for deep research
        result = await asyncio.wait_for(
            client.create_completion(messages),
            timeout=60.0  # 60 seconds for deep research
        )
        
        output = PerplexityResearchResult(answer=result["response"])
        logger.info(f"perplexity_deep_research completed successfully in {time.time() - start_time:.2f}s")
        
        return output.model_dump()
        
    except ValidationError as exc:
        logger.error(f"Input validation failed: {exc}")
        raise ValueError(f"Invalid input for perplexity_deep_research: {exc}")
    except asyncio.TimeoutError:
        logger.error(f"Deep research timed out after 60s")
        raise TimeoutError("Perplexity deep research timed out after 60 seconds")
    except Exception as e:
        logger.error(f"perplexity_deep_research failed after {time.time() - start_time:.2f}s: {e}")
        raise

# Diagnostic runner
async def run_diagnostics():
    """Run all diagnostic tests."""
    print("=== MCP Perplexity Tools Diagnostics ===\n")
    
    # Test 1: Direct LLM client
    print("1. Testing direct LLM client...")
    direct_success = await test_llm_client_direct()
    print(f"   Result: {'✓ PASS' if direct_success else '✗ FAIL'}\n")
    
    if not direct_success:
        print("Direct client test failed. Check your chuk-llm configuration.")
        return
    
    # Test 2: Isolated function test
    print("2. Testing isolated perplexity_search function...")
    isolated_result = await test_perplexity_search_isolated()
    isolated_success = isolated_result is not None
    print(f"   Result: {'✓ PASS' if isolated_success else '✗ FAIL'}")
    if isolated_success:
        print(f"   Response: {isolated_result['answer'][:100]}...")
    print()
    
    # Test 3: Improved function test
    print("3. Testing improved perplexity_search function...")
    try:
        improved_result = await improved_perplexity_search("What is the capital of France?")
        print(f"   Result: ✓ PASS")
        print(f"   Response: {improved_result['answer'][:100]}...")
    except Exception as e:
        print(f"   Result: ✗ FAIL - {e}")
    
    print("\n=== Diagnostics Complete ===")

if __name__ == "__main__":
    asyncio.run(run_diagnostics())