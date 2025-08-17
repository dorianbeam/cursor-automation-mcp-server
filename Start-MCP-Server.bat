@echo off
title Cursor Automation Builder MCP Server

echo.
echo ========================================
echo  Cursor Automation Builder MCP Server
echo ========================================
echo.
echo 🚀 Starting MCP server...
echo 📍 Project: %~dp0
echo 🎯 Server will be available for MCP clients
echo 💡 Press Ctrl+C to stop the server
echo.

REM Change to script directory
cd /d "%~dp0"

REM Start MCP server
python -m app.mcp.mcp

echo.
echo 🛑 MCP server stopped.
echo.
pause