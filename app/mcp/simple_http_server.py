# app/mcp/simple_http_server.py
"""
Simple HTTP wrapper for FastMCP server
Compatible with various MCP versions
"""

import asyncio
import json
import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .server import mcp

# Create FastAPI app
app = FastAPI(
    title="Cursor Automation System Builder MCP Server",
    description="HTTP-accessible MCP server for automation system building",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/")
async def root():
    tools = []
    try:
        # Get tools from FastMCP server
        tools = list(mcp._tools.keys()) if hasattr(mcp, '_tools') else []
    except:
        pass
    
    return {
        "message": "Cursor Automation System Builder MCP Server",
        "status": "running",
        "mcp_endpoints": {
            "tools": "/mcp/tools",
            "call": "/mcp/call"
        },
        "tools_available": len(tools),
        "tools": tools
    }

@app.get("/health")
async def health():
    tools = []
    try:
        tools = list(mcp._tools.keys()) if hasattr(mcp, '_tools') else []
    except:
        pass
    
    return {
        "status": "healthy", 
        "tools_available": len(tools),
        "server": "cursor-automation-builder"
    }

# MCP Tools endpoint
@app.get("/mcp/tools")
async def list_tools():
    """List all available MCP tools"""
    try:
        tools = []
        if hasattr(mcp, '_tools'):
            for name, tool in mcp._tools.items():
                tool_info = {
                    "name": name,
                    "description": getattr(tool, '__doc__', 'No description available')
                }
                # Try to get input schema if available
                if hasattr(tool, '__annotations__'):
                    tool_info["parameters"] = str(tool.__annotations__)
                tools.append(tool_info)
        
        return {
            "tools": tools,
            "count": len(tools)
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Failed to list tools: {str(e)}"}
        )

# MCP Tool call endpoint
@app.post("/mcp/call/{tool_name}")
async def call_tool(tool_name: str, request: Request):
    """Call an MCP tool"""
    try:
        # Get request body
        body = await request.json()
        
        # Check if tool exists
        if not hasattr(mcp, '_tools') or tool_name not in mcp._tools:
            raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")
        
        # Get the tool function
        tool_func = mcp._tools[tool_name]
        
        # Call the tool
        if asyncio.iscoroutinefunction(tool_func):
            result = await tool_func(**body)
        else:
            result = tool_func(**body)
        
        return {
            "tool": tool_name,
            "result": result,
            "status": "success"
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "tool": tool_name,
                "error": str(e),
                "status": "error"
            }
        )

# Generic MCP endpoint for protocol compatibility
@app.post("/mcp")
async def mcp_protocol(request: Request):
    """Handle MCP protocol requests"""
    try:
        body = await request.json()
        method = body.get('method', '')
        params = body.get('params', {})
        
        if method == 'tools/list':
            return await list_tools()
        
        elif method == 'tools/call':
            tool_name = params.get('name', '')
            arguments = params.get('arguments', {})
            request_body = type('Request', (), {'json': lambda: arguments})()
            return await call_tool(tool_name, request_body)
        
        else:
            return JSONResponse(
                status_code=400,
                content={"error": f"Unsupported method: {method}"}
            )
            
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"MCP protocol error: {str(e)}"}
        )

if __name__ == "__main__":
    uvicorn.run(
        "app.mcp.simple_http_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
