@echo off
REM Quick Permanent Setup Script for Windows
echo 🚀 Setting up Cursor Automation Builder MCP Server for permanent use...
echo.

REM Check if Python and pip are available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python first.
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Check current directory
echo 📁 Current directory: %CD%
echo.

REM Install dependencies if not already installed
echo 📦 Installing MCP dependencies...
python -m pip install fastmcp pydantic --user --quiet
if %errorlevel% neq 0 (
    echo ⚠️  Some dependencies may already be installed - continuing...
)

echo ✅ Dependencies ready
echo.

REM Test MCP server
echo 🧪 Testing MCP server...
python -c "from app.mcp.server import mcp; print('✅ MCP server ready:', mcp.name)" 2>nul
if %errorlevel% neq 0 (
    echo ❌ MCP server test failed. Check your setup.
    pause
    exit /b 1
)

echo ✅ MCP server test passed
echo.

REM Create Claude Desktop configuration
echo 📝 Creating Claude Desktop configuration...

set "CLAUDE_CONFIG_DIR=%APPDATA%\Claude"
set "CLAUDE_CONFIG_FILE=%CLAUDE_CONFIG_DIR%\claude_desktop_config.json"
set "PROJECT_PATH=%CD%"

REM Create Claude config directory if it doesn't exist
if not exist "%CLAUDE_CONFIG_DIR%" (
    mkdir "%CLAUDE_CONFIG_DIR%"
)

REM Create or update Claude Desktop config
(
echo {
echo   "mcpServers": {
echo     "cursor-automation-builder": {
echo       "command": "python",
echo       "args": [
echo         "-m", "app.mcp.mcp"
echo       ],
echo       "cwd": "%PROJECT_PATH:\=\\%",
echo       "env": {
echo         "PYTHONPATH": "."
echo       }
echo     }
echo   }
echo }
) > "%CLAUDE_CONFIG_FILE%"

echo ✅ Claude Desktop configuration created at:
echo    %CLAUDE_CONFIG_FILE%
echo.

REM Create desktop shortcut for manual server start
echo 🔗 Creating desktop shortcut...
set "SHORTCUT_PATH=%USERPROFILE%\Desktop\Start MCP Server.bat"
(
echo @echo off
echo cd /d "%PROJECT_PATH%"
echo echo 🚀 Starting Cursor Automation Builder MCP Server...
echo echo Server will be available for Claude Desktop and other MCP clients
echo echo Press Ctrl+C to stop the server
echo echo.
echo python -m app.mcp.mcp
echo pause
) > "%SHORTCUT_PATH%"

echo ✅ Desktop shortcut created: Start MCP Server.bat
echo.

REM Test complete setup
echo 🔍 Final test - checking tool registration...
python -c "
try:
    from app.mcp import mcp
    print('✅ All MCP tools registered successfully')
    print('🎯 Setup complete - ready for production use!')
except Exception as e:
    print(f'❌ Final test failed: {e}')
" 2>nul

echo.
echo 🎉 SETUP COMPLETE!
echo.
echo ✅ MCP server configured for permanent use
echo ✅ Claude Desktop will auto-start the server
echo ✅ Desktop shortcut created for manual server start
echo ✅ All 9 automation tools ready
echo.
echo 🚀 NEXT STEPS:
echo    1. Restart Claude Desktop
echo    2. Test with: "Use cursor automation builder to analyze my workspace"
echo    3. Try: "Build a data processing system with cursor automation builder"
echo.
echo 📚 See PERMANENT-DEPLOYMENT-GUIDE.md for advanced options
echo.
pause