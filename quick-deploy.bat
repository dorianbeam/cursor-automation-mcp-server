@echo off
REM Quick deployment script for Cursor Automation System Builder MCP Server
echo 🎯 Cursor Automation System Builder - Quick Deploy
echo =================================================

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    pause
    exit /b 1
)

echo ✅ Python found

REM Install requirements
echo 📦 Installing requirements...
python -m pip install -r mcp_requirements.txt

if %errorlevel% neq 0 (
    echo ❌ Failed to install requirements
    pause
    exit /b 1
)

echo ✅ Requirements installed

REM Start deployment wizard
echo 🚀 Starting deployment wizard...
python deploy.py

pause
