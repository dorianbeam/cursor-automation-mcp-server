# app/mcp/server.py
from fastmcp import FastMCP

mcp = FastMCP(
    name="Cursor Automation System Builder",
    instructions="""
    The Cursor Automation System Builder MCP server provides intelligent automation system creation capabilities.
    
    Core capabilities:
    - Build complete automation systems from descriptions
    - Template-based system creation with proven patterns
    - Intelligent workspace analysis and enhancement suggestions
    - Progressive learning tutorials and guided building
    - Meta-optimization for continuous system improvement
    - Auto-template generation from successful builds
    
    The system operates in three adaptive modes:
    - BUILD_MODE: Efficiency-focused direct system creation
    - LEARN_MODE: Educational building with detailed explanations
    - BALANCED: Adaptive approach balancing efficiency with learning
    
    All tools provide immediate, production-ready automation systems with built-in enhancements
    like validation, error handling, progress tracking, and professional reporting.
    """
)