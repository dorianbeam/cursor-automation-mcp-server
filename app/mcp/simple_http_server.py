# app/mcp/simple_http_server.py
"""
HTTP/SSE wrapper for FastMCP server - Railway Compatible
Supports both HTTP and Server-Sent Events (SSE) for Cursor MCP integration
"""

import asyncio
import json
import uvicorn
import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from .server import mcp
from .mcp import register_all_tools

# Ensure tools are registered
register_all_tools(mcp)

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

# SSE endpoint for Cursor MCP integration
@app.get("/sse")
async def sse_endpoint():
    """Server-Sent Events endpoint for Cursor MCP integration"""
    
    async def generate_events():
        # Initial connection event
        yield f"data: {json.dumps({'type': 'init', 'message': 'MCP Server Connected'})}\n\n"
        
        # Send available tools
        tools = []
        try:
            if hasattr(mcp, '_tools') and mcp._tools:
                tools = [
                    {
                        "name": name,
                        "description": getattr(tool, '__doc__', 'No description available'),
                        "parameters": getattr(tool, '__annotations__', {})
                    }
                    for name, tool in mcp._tools.items()
                ]
            else:
                # Fallback tool list
                tools = [
                    {"name": "build_automation_system", "description": "Build complete automation systems from descriptions"},
                    {"name": "list_automation_templates", "description": "List available automation templates"},
                    {"name": "build_from_template", "description": "Build systems using proven templates"},
                    {"name": "start_learning_path", "description": "Start guided learning tutorials"},
                    {"name": "meta_optimize_system", "description": "Optimize and analyze system performance"},
                    {"name": "analyze_workspace", "description": "Analyze workspace for automation opportunities"},
                    {"name": "list_templates", "description": "List all available templates"},
                    {"name": "get_template_details", "description": "Get detailed template information"},
                    {"name": "create_custom_template", "description": "Create custom templates"}
                ]
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'message': f'Tools error: {str(e)}'})}\n\n"
        
        yield f"data: {json.dumps({'type': 'tools', 'tools': tools})}\n\n"
        
        # Keep connection alive
        while True:
            yield f"data: {json.dumps({'type': 'heartbeat', 'timestamp': asyncio.get_event_loop().time()})}\n\n"
            await asyncio.sleep(30)  # Heartbeat every 30 seconds
    
    return StreamingResponse(
        generate_events(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*"
        }
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
        "version": "1.0.0",
        "mcp_endpoints": {
            "sse": "/sse",
            "tools": "/mcp/tools",
            "call": "/mcp/call",
            "protocol": "/mcp"
        },
        "tools_available": len(tools),
        "tools": tools,
        "railway_compatible": True
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
        # Try different ways to access FastMCP tools
        tools = []
        
        # Method 1: Check for _tools attribute
        if hasattr(mcp, '_tools') and mcp._tools:
            for name, tool in mcp._tools.items():
                tool_info = {
                    "name": name,
                    "description": getattr(tool, '__doc__', 'No description available')
                }
                if hasattr(tool, '__annotations__'):
                    tool_info["parameters"] = str(tool.__annotations__)
                tools.append(tool_info)
        
        # Method 2: Try to get tools from FastMCP instance
        elif hasattr(mcp, 'list_tools'):
            try:
                mcp_tools = await mcp.list_tools() if asyncio.iscoroutinefunction(mcp.list_tools) else mcp.list_tools()
                if isinstance(mcp_tools, (list, tuple)):
                    tools = [{"name": tool, "description": f"FastMCP tool: {tool}"} for tool in mcp_tools]
                elif isinstance(mcp_tools, dict):
                    tools = [{"name": name, "description": info.get('description', 'FastMCP tool')} 
                            for name, info in mcp_tools.items()]
            except Exception as e:
                pass
        
        # Method 3: Hardcoded tool list as fallback (your 9 known tools)
        if not tools:
            tools = [
                {"name": "build_automation_system", "description": "Build complete automation systems from descriptions"},
                {"name": "list_automation_templates", "description": "List available automation templates"},
                {"name": "build_from_template", "description": "Build systems using proven templates"},
                {"name": "start_learning_path", "description": "Start guided learning tutorials"},
                {"name": "meta_optimize_system", "description": "Optimize and analyze system performance"},
                {"name": "analyze_workspace", "description": "Analyze workspace for automation opportunities"},
                {"name": "list_templates", "description": "List all available templates"},
                {"name": "get_template_details", "description": "Get detailed template information"},
                {"name": "create_custom_template", "description": "Create custom templates"}
            ]
        
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
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "app.mcp.simple_http_server:app",
        host="0.0.0.0",
        port=port,
        reload=False  # Disable reload in production
    )
