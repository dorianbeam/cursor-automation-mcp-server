# app/mcp/mcp.py
import logging
from fastmcp import FastMCP
from app.mcp.server import mcp

logger = logging.getLogger("cursor_automation_builder_mcp")

def register_all_tools(server_instance: FastMCP) -> None:
    """
    Register all available tools with the FastMCP server.
    This function triggers tool registration by importing the modules
    where @server_instance.tool() decorators are used.

    Args:
        server_instance: The FastMCP instance to which tools are registered.
    """
    logger.info(f"Registering all MCP tools for server: {server_instance.name}")
    
    # Import tool modules here to trigger decorator-based registration
    # Make sure we're importing with the correct server instance
    try:
        # Force reload to ensure decorators are applied to this server instance
        import importlib
        import sys
        
        # Remove from cache if already imported
        modules_to_reload = [
            'app.mcp.tools.automation_builder.automation_builder',
            'app.mcp.tools.workspace_analyzer.workspace_analyzer', 
            'app.mcp.tools.template_manager.template_manager'
        ]
        
        for module_name in modules_to_reload:
            if module_name in sys.modules:
                del sys.modules[module_name]
        
        # Now import fresh with decorators
        import app.mcp.tools.automation_builder.automation_builder  # noqa: F401
        logger.info("✅ Automation builder tools imported")
        
        import app.mcp.tools.workspace_analyzer.workspace_analyzer  # noqa: F401
        logger.info("✅ Workspace analyzer tools imported")
        
        import app.mcp.tools.template_manager.template_manager  # noqa: F401
        logger.info("✅ Template manager tools imported")
        
    except ImportError as e:
        logger.error(f"❌ Failed to register tools: {e}")
    except Exception as e:
        logger.error(f"❌ Unexpected error during tool registration: {e}")
    
    logger.info("Tool registration process completed")

# Call registration function, passing the imported mcp instance
register_all_tools(mcp)

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger.info(f"🚀 Starting MCP server: {mcp.name}")
    logger.info("Available tools:")
    
    # List registered tools using FastMCP's get_tools method
    tool_count = 0
    try:
        import asyncio
        # Get tools using async/await properly
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        tools = loop.run_until_complete(mcp.get_tools())
        loop.close()
        
        if tools:
            for tool in tools:
                tool_name = tool.name if hasattr(tool, 'name') else str(tool)
                logger.info(f"  • {tool_name}")
                tool_count += 1
        else:
            logger.info("  No tools found via get_tools()")
    except Exception as e:
        logger.error(f"Error getting tools: {e}")
        logger.info("  Checking tool registration status...")
        
        # Check if tools are registered by testing imports
        expected_tools = [
            ('build_automation_system', 'app.mcp.tools.automation_builder.automation_builder'),
            ('list_automation_templates', 'app.mcp.tools.automation_builder.automation_builder'),
            ('build_from_template', 'app.mcp.tools.automation_builder.automation_builder'),
            ('start_learning_path', 'app.mcp.tools.automation_builder.automation_builder'),
            ('meta_optimize_system', 'app.mcp.tools.automation_builder.automation_builder'),
            ('analyze_workspace', 'app.mcp.tools.workspace_analyzer.workspace_analyzer'),
            ('list_templates', 'app.mcp.tools.template_manager.template_manager'),
            ('get_template_details', 'app.mcp.tools.template_manager.template_manager'),
            ('create_custom_template', 'app.mcp.tools.template_manager.template_manager')
        ]
        
        for tool_name, module_path in expected_tools:
            try:
                module = __import__(module_path, fromlist=[tool_name])
                if hasattr(module, tool_name):
                    logger.info(f"  • {tool_name} (function exists in {module_path})")
                    tool_count += 1
                else:
                    logger.warning(f"  ✗ {tool_name} (not found in {module_path})")
            except ImportError as ie:
                logger.error(f"  ✗ {tool_name} - Import error: {ie}")
    
    logger.info(f"Total tools registered: {tool_count}")
    logger.info("🌟 Cursor Automation System Builder MCP Server ready!")
    
    # Start the server
    mcp.run()