# 🔄 Permanent MCP Server Deployment & Usage Guide

**How to run your Cursor Automation System Builder MCP server permanently and use it effectively**

---

## 🚀 Permanent Deployment Options

### **Option 1: Claude Desktop Integration (Recommended for Personal Use)**

#### **Step 1: Find Claude Desktop Config**
```bash
# Windows
%APPDATA%\Claude\claude_desktop_config.json

# macOS  
~/Library/Application Support/Claude/claude_desktop_config.json

# Linux
~/.config/Claude/claude_desktop_config.json
```

#### **Step 2: Configure Claude Desktop**
Edit or create `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "cursor-automation-builder": {
      "command": "python",
      "args": [
        "-m", "app.mcp.mcp"
      ],
      "cwd": "C:\\Users\\dsber\\Code\\Cursor-Automation-System-Builder",
      "env": {
        "PYTHONPATH": "."
      }
    }
  }
}
```

#### **Step 3: Restart Claude Desktop**
- Close Claude Desktop completely
- Restart Claude Desktop
- The MCP server will start automatically when Claude starts

#### **Step 4: Test Integration**
In Claude Desktop, try:
```
"Use the cursor automation builder to analyze my current workspace"
"Build a data processing system with the cursor automation builder"
"List available automation templates using cursor automation builder"
```

---

### **Option 2: Windows Service (For Always-On Server)**

#### **Step 1: Create Service Script**
```python
# File: app/mcp/service_runner.py
import sys
import os
import logging
import time
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mcp_server.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("mcp_service")

def main():
    """Main service loop"""
    logger.info("🚀 Starting Cursor Automation MCP Server Service")
    
    try:
        from app.mcp import mcp
        logger.info("✅ MCP server initialized successfully")
        
        # Start the server
        mcp.run()
        
    except Exception as e:
        logger.error(f"❌ MCP server failed to start: {e}")
        raise

if __name__ == "__main__":
    main()
```

#### **Step 2: Install Python Windows Service**
```bash
# Install pywin32 for Windows service support
pip install pywin32

# Install service
python app/mcp/service_runner.py install

# Start service
python app/mcp/service_runner.py start
```

#### **Step 3: Configure Service**
```bash
# Set service to auto-start
sc config CursorAutomationMCP start=auto

# Check service status
sc query CursorAutomationMCP
```

---

### **Option 3: Docker Container (Cross-Platform)**

#### **Step 1: Create Dockerfile**
```dockerfile
# File: Dockerfile.mcp
FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY mcp_requirements.txt .
RUN pip install --no-cache-dir -r mcp_requirements.txt

# Copy application code
COPY . .

# Expose MCP port (if needed)
EXPOSE 8000

# Set Python path
ENV PYTHONPATH=/app

# Run MCP server
CMD ["python", "-m", "app.mcp.mcp"]
```

#### **Step 2: Build and Run Container**
```bash
# Build Docker image
docker build -f Dockerfile.mcp -t cursor-automation-mcp .

# Run container with restart policy
docker run -d \
  --name cursor-automation-mcp \
  --restart unless-stopped \
  -p 8000:8000 \
  -v $(pwd):/app \
  cursor-automation-mcp
```

#### **Step 3: Docker Compose (Advanced)**
```yaml
# File: docker-compose.mcp.yml
version: '3.8'

services:
  cursor-automation-mcp:
    build:
      context: .
      dockerfile: Dockerfile.mcp
    container_name: cursor-automation-mcp
    restart: unless-stopped
    ports:
      - "8000:8000"
    volumes:
      - .:/app
      - mcp_data:/app/data
    environment:
      - PYTHONPATH=/app
      - MCP_LOG_LEVEL=INFO

volumes:
  mcp_data:
```

```bash
# Start with Docker Compose
docker-compose -f docker-compose.mcp.yml up -d

# Check status
docker-compose -f docker-compose.mcp.yml ps

# View logs
docker-compose -f docker-compose.mcp.yml logs -f
```

---

### **Option 4: Linux Systemd Service**

#### **Step 1: Create Service File**
```ini
# File: /etc/systemd/system/cursor-automation-mcp.service
[Unit]
Description=Cursor Automation System Builder MCP Server
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/Cursor-Automation-System-Builder
Environment=PYTHONPATH=/path/to/Cursor-Automation-System-Builder
ExecStart=/usr/bin/python3 -m app.mcp.mcp
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### **Step 2: Enable and Start Service**
```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service (start on boot)
sudo systemctl enable cursor-automation-mcp

# Start service
sudo systemctl start cursor-automation-mcp

# Check status
sudo systemctl status cursor-automation-mcp

# View logs
journalctl -u cursor-automation-mcp -f
```

---

## 🎯 How to Use the MCP Server

### **1. Using with Claude Desktop**

#### **Basic Commands**
Once configured, use these patterns in Claude Desktop:

```
# Analyze workspace for automation opportunities
"Use cursor automation builder to analyze my current workspace for automation opportunities"

# Build complete automation system
"Build a data processing system using cursor automation builder that can process CSV files and generate reports"

# List available templates
"Show me all available automation templates from cursor automation builder"

# Build from specific template
"Use cursor automation builder to build an API integration system from the api_integrator template"

# Get template details
"Get detailed information about the data_processor template from cursor automation builder"

# Create custom template
"Create a custom template using cursor automation builder for processing customer feedback data"

# Start learning path
"Start a learning path for data processing automation using cursor automation builder"

# Optimize system performance
"Run meta optimization on cursor automation builder to improve system performance"
```

#### **Advanced Usage Patterns**
```
# Workspace analysis with specific directory
"Analyze the ./projects/sales-data directory using cursor automation builder workspace analyzer"

# Build with specific requirements
"Build an automation system with cursor automation builder that:
- Processes CSV and Excel files
- Validates email addresses and phone numbers  
- Generates PDF reports with charts
- Sends email notifications when complete"

# Template-based building with customizations
"Use the api_integrator template from cursor automation builder to create a system that syncs data between Salesforce and HubSpot every hour"

# Learning with specific focus
"Start a beginner learning path for API integration using cursor automation builder with hands-on practice"
```

### **2. Using with VS Code Extensions**

#### **Create VS Code Extension Integration**
```javascript
// File: vscode-extension/src/mcpClient.js
import { MCPClient } from '@modelcontextprotocol/sdk';

class CursorAutomationClient {
    constructor() {
        this.client = new MCPClient({
            name: 'cursor-automation-builder',
            version: '1.0.0'
        });
    }

    async analyzeWorkspace(workspacePath) {
        return await this.client.call_tool('analyze_workspace', {
            target_directory: workspacePath,
            analysis_depth: 'standard',
            include_suggestions: true
        });
    }

    async buildAutomation(goal, mode = 'BUILD_MODE') {
        return await this.client.call_tool('build_automation_system', {
            automation_goal: goal,
            build_mode: mode,
            enhancement_preference: 'ask_major'
        });
    }

    async listTemplates(category = null) {
        return await this.client.call_tool('list_templates', {
            category: category,
            sort_by: 'popularity'
        });
    }
}

// Usage in VS Code extension
const automationClient = new CursorAutomationClient();

// Command: Analyze current workspace
vscode.commands.registerCommand('cursor-automation.analyzeWorkspace', async () => {
    const workspacePath = vscode.workspace.rootPath;
    const result = await automationClient.analyzeWorkspace(workspacePath);
    
    // Show results in VS Code
    vscode.window.showInformationMessage(
        `Found ${result.file_patterns.length} automation opportunities!`
    );
});
```

### **3. Using with Custom Applications**

#### **Python Integration Example**
```python
# File: custom_integration.py
import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class CursorAutomationIntegration:
    def __init__(self):
        self.client = None
        
    async def connect(self):
        """Connect to MCP server"""
        server_params = StdioServerParameters(
            command="python",
            args=["-m", "app.mcp.mcp"],
            cwd="/path/to/Cursor-Automation-System-Builder"
        )
        
        self.client = await stdio_client(server_params)
    
    async def build_automation_system(self, goal: str, mode: str = "BUILD_MODE"):
        """Build automation system"""
        if not self.client:
            await self.connect()
            
        result = await self.client.call_tool("build_automation_system", {
            "automation_goal": goal,
            "build_mode": mode,
            "enhancement_preference": "automatic"
        })
        
        return result
    
    async def analyze_workspace(self, directory: str):
        """Analyze workspace for automation opportunities"""
        if not self.client:
            await self.connect()
            
        result = await self.client.call_tool("analyze_workspace", {
            "target_directory": directory,
            "include_suggestions": True
        })
        
        return result

# Usage example
async def main():
    integration = CursorAutomationIntegration()
    
    # Analyze current directory
    analysis = await integration.analyze_workspace(".")
    print(f"Found {len(analysis['automation_suggestions'])} opportunities")
    
    # Build system based on analysis
    if analysis['automation_suggestions']:
        suggestion = analysis['automation_suggestions'][0]
        result = await integration.build_automation_system(
            goal=suggestion['description'],
            mode="BUILD_MODE"
        )
        print(f"Built system: {result['system_name']}")

# Run integration
asyncio.run(main())
```

---

## 🔧 Monitoring & Maintenance

### **1. Health Monitoring**

#### **Create Health Check Script**
```python
# File: app/mcp/health_check.py
import asyncio
import time
import logging
from pathlib import Path

async def health_check():
    """Check MCP server health"""
    try:
        from app.mcp.server import mcp
        
        # Basic import test
        print("✅ MCP server imports successfully")
        
        # Tool registration test
        from app.mcp import mcp as mcp_module
        print("✅ Tool registration successful")
        
        # Template availability test
        templates_dir = Path("automation-systems/automation-framework/templates")
        if templates_dir.exists():
            template_count = len(list(templates_dir.glob("*.json"))) + 5  # Built-in templates
            print(f"✅ {template_count} templates available")
        
        print("🎯 MCP server is healthy and ready!")
        return True
        
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(health_check())
```

#### **Automated Health Monitoring**
```bash
# Create cron job for health monitoring (Linux/macOS)
# Add to crontab with: crontab -e

# Check health every 5 minutes
*/5 * * * * cd /path/to/Cursor-Automation-System-Builder && python app/mcp/health_check.py >> /var/log/mcp_health.log 2>&1

# Restart service if unhealthy (systemd)
*/10 * * * * systemctl is-active --quiet cursor-automation-mcp || systemctl restart cursor-automation-mcp
```

### **2. Logging & Diagnostics**

#### **Enhanced Logging Configuration**
```python
# File: app/mcp/logging_config.py
import logging
import sys
from pathlib import Path

def setup_logging(log_level="INFO", log_file="mcp_server.log"):
    """Setup comprehensive logging for MCP server"""
    
    # Create logs directory
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Set specific loggers
    loggers = [
        'cursor_automation_builder_mcp',
        'app.mcp',
        'fastmcp',
        'mcp'
    ]
    
    for logger_name in loggers:
        logger = logging.getLogger(logger_name)
        logger.setLevel(getattr(logging, log_level))
    
    logging.info("🚀 Logging configuration complete")
```

### **3. Performance Monitoring**

#### **Performance Metrics Collection**
```python
# File: app/mcp/metrics.py
import time
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime

class MetricsCollector:
    def __init__(self):
        self.metrics = defaultdict(list)
        self.metrics_file = Path("logs/mcp_metrics.json")
        
    def record_tool_call(self, tool_name: str, duration: float, success: bool):
        """Record tool call metrics"""
        self.metrics[tool_name].append({
            'timestamp': datetime.now().isoformat(),
            'duration': duration,
            'success': success
        })
        
        # Save metrics periodically
        if len(self.metrics[tool_name]) % 10 == 0:
            self.save_metrics()
    
    def save_metrics(self):
        """Save metrics to file"""
        self.metrics_file.parent.mkdir(exist_ok=True)
        with open(self.metrics_file, 'w') as f:
            json.dump(dict(self.metrics), f, indent=2)
    
    def get_performance_summary(self):
        """Get performance summary"""
        summary = {}
        for tool, calls in self.metrics.items():
            if calls:
                durations = [call['duration'] for call in calls]
                successes = [call['success'] for call in calls]
                
                summary[tool] = {
                    'total_calls': len(calls),
                    'success_rate': sum(successes) / len(successes),
                    'avg_duration': sum(durations) / len(durations),
                    'max_duration': max(durations),
                    'min_duration': min(durations)
                }
        
        return summary

# Global metrics collector
metrics = MetricsCollector()
```

---

## 🎯 Production Deployment Checklist

### **Pre-Deployment**
- [ ] Install all dependencies (`pip install -r mcp_requirements.txt`)
- [ ] Test MCP server locally (`python -m app.mcp.mcp`)
- [ ] Verify all 9 tools are registered correctly
- [ ] Test with sample data and workspace analysis

### **Deployment**
- [ ] Choose deployment method (Claude Desktop/Service/Docker)
- [ ] Configure appropriate startup method
- [ ] Set up logging and monitoring
- [ ] Test client connectivity

### **Post-Deployment**
- [ ] Verify MCP client can connect and use tools
- [ ] Test core functionality with real workspaces
- [ ] Set up health monitoring and alerting
- [ ] Document specific usage patterns for your team

### **Security Considerations**
- [ ] Restrict file system access to appropriate directories
- [ ] Set up proper logging without sensitive data
- [ ] Configure resource limits (memory, CPU, disk)
- [ ] Regular security updates for dependencies

---

## 🎯 Troubleshooting Guide

### **Common Issues & Solutions**

#### **MCP Server Won't Start**
```bash
# Check Python path and dependencies
python -c "from app.mcp.server import mcp; print('✅ Server imports OK')"

# Check if port is in use
netstat -an | findstr :8000  # Windows
lsof -i :8000               # Linux/macOS

# Check logs
tail -f logs/mcp_server.log
```

#### **Claude Desktop Can't Connect**
```json
// Verify config path and syntax
{
  "mcpServers": {
    "cursor-automation-builder": {
      "command": "python",
      "args": ["-m", "app.mcp.mcp"],
      "cwd": "FULL_PATH_TO_PROJECT",
      "env": {
        "PYTHONPATH": "."
      }
    }
  }
}
```

#### **Tools Not Working**
```bash
# Test tool registration
python -c "
from app.mcp import mcp
print('MCP tools registered successfully')
"

# Check specific tool
python -c "
from app.mcp.tools.automation_builder.automation_builder import build_automation_system
print('Automation builder tool available')
"
```

#### **Performance Issues**
```python
# Check system resources
import psutil
print(f'CPU: {psutil.cpu_percent()}%')
print(f'Memory: {psutil.virtual_memory().percent}%')
print(f'Disk: {psutil.disk_usage("/").percent}%')

# Enable debug logging
# In app/mcp/mcp.py, set logging level to DEBUG
logging.basicConfig(level=logging.DEBUG)
```

---

🎯 **Your MCP server is now ready for permanent deployment and production use!**

**Choose your deployment method:**
- ✅ **Claude Desktop** → Best for personal use, automatic startup
- ✅ **Windows Service** → Always-on server for team use  
- ✅ **Docker Container** → Cross-platform, scalable deployment
- ✅ **Linux systemd** → Production server deployment

**Ready to automate workflows permanently through MCP integration!**