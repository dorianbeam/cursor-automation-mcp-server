# app/mcp/http_server.py
import asyncio
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
try:
    from mcp.server.fastapi import MCPFastAPIAdapter
except ImportError:
    # Fallback for different MCP versions
    from mcp.server import Server as MCPFastAPIAdapter
from .server import mcp

# Create FastAPI app
app = FastAPI(
    title="Cursor Automation System Builder MCP Server",
    description="HTTP-accessible MCP server for automation system building",
    version="1.0.0"
)

# Add CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create MCP adapter
mcp_adapter = MCPFastAPIAdapter(mcp)

# Mount MCP endpoints
app.mount("/mcp", mcp_adapter.app)

# Health check endpoint
@app.get("/")
async def root():
    return {
        "message": "Cursor Automation System Builder MCP Server",
        "status": "running",
        "mcp_endpoint": "/mcp",
        "tools": len(mcp.list_tools())
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "tools_available": len(mcp.list_tools())}

if __name__ == "__main__":
    uvicorn.run(
        "app.mcp.http_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
