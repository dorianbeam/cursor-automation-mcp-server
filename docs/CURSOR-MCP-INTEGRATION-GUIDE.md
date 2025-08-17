# 🔧 Cursor MCP Integration Guide

**Add your Cursor Automation System Builder to Cursor's MCP configuration**

---

## 🎯 Add to Your Cursor MCP Configuration

### **Your Current `.cursor/mcp.json` Location**
```
C:\Users\dsber\.cursor\mcp.json
```

### **Updated Configuration**
Add this to your existing `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "n8n-mcp": {
      "command": "npx",
      "args": [
        "n8n-mcp"
      ],
      "env": {
        "MCP_MODE": "stdio",
        "LOG_LEVEL": "error",
        "DISABLE_CONSOLE_OUTPUT": "true",
        "N8N_API_URL": "https://beamai.app.n8n.cloud/",
        "N8N_API_KEY": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI4MDczNGFjNS05MTU5LTQwYmItYjZmOS1mODJmMWEyNTI4NzQiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzUyNTgwNjA3LCJleHAiOjE3NTUxMjI0MDB9.YAtg52VnR0mjylOHRObrFf1t5rf_NNmoXpxdpOrzOcI"
      }
    },
    "linear": {
      "url": "https://mcp.linear.app/sse"
    },
    "airtable": {
      "command": "npx",
      "args": [
        "-y",
        "airtable-mcp-server"
      ],
      "env": {
        "AIRTABLE_API_KEY": "patJS9Hojd6kd1SGM.2ff1fc95bb3dd96fac2ad5f191514500c15c48488817843da3055c04aec4dc81"
      }
    },
    "vercel": {
      "url": "https://mcp.vercel.com",
      "headers": {}
    },
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

---

## 🚀 How to Make Available to Others

### **Method 1: Direct Repository Sharing**

#### **Step 1: Create Distribution Package**
```bash
# Create a distributable package
mkdir cursor-automation-builder-mcp
cp -r app/ cursor-automation-builder-mcp/
cp -r automation-systems/ cursor-automation-builder-mcp/
cp mcp_requirements.txt cursor-automation-builder-mcp/
cp MCP-SETUP-GUIDE.md cursor-automation-builder-mcp/
cp READY-TO-USE-SUMMARY.md cursor-automation-builder-mcp/
```

#### **Step 2: Create Setup Instructions**
Users would:
1. Clone/download your repository
2. Install dependencies: `pip install -r mcp_requirements.txt`
3. Add to their `.cursor/mcp.json` with their own path

### **Method 2: NPM Package (Recommended)**

#### **Step 1: Create NPM Package Structure**
```javascript
// package.json
{
  "name": "cursor-automation-builder-mcp",
  "version": "1.0.0",
  "description": "Intelligent automation system builder for Cursor via MCP",
  "main": "dist/index.js",
  "bin": {
    "cursor-automation-builder-mcp": "dist/server.js"
  },
  "scripts": {
    "start": "python -m app.mcp.mcp",
    "install-deps": "pip install -r mcp_requirements.txt"
  },
  "keywords": ["mcp", "cursor", "automation", "ai"],
  "author": "Your Name",
  "license": "MIT",
  "dependencies": {
    "cross-spawn": "^7.0.3"
  }
}
```

#### **Step 2: Create Node.js Wrapper**
```javascript
// dist/server.js
#!/usr/bin/env node
const spawn = require('cross-spawn');
const path = require('path');

// Get the directory where this package is installed
const packageDir = __dirname;
const projectRoot = path.join(packageDir, '..');

// Start the Python MCP server
const pythonProcess = spawn('python', ['-m', 'app.mcp.mcp'], {
  cwd: projectRoot,
  env: {
    ...process.env,
    PYTHONPATH: projectRoot
  },
  stdio: 'inherit'
});

process.on('SIGINT', () => {
  pythonProcess.kill('SIGINT');
});

process.on('SIGTERM', () => {
  pythonProcess.kill('SIGTERM');
});
```

#### **Step 3: Publish to NPM**
```bash
npm publish cursor-automation-builder-mcp
```

#### **Step 4: Users Install via NPM**
```bash
# Users install globally
npm install -g cursor-automation-builder-mcp

# Add to their .cursor/mcp.json
{
  "mcpServers": {
    "cursor-automation-builder": {
      "command": "cursor-automation-builder-mcp"
    }
  }
}
```

### **Method 3: Docker Container Distribution**

#### **Step 1: Create Production Dockerfile**
```dockerfile
# Dockerfile.production
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY mcp_requirements.txt .
RUN pip install --no-cache-dir -r mcp_requirements.txt

# Copy application code
COPY app/ ./app/
COPY automation-systems/ ./automation-systems/

# Set environment
ENV PYTHONPATH=/app
ENV MCP_LOG_LEVEL=INFO

# Expose MCP port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
  CMD python -c "from app.mcp.server import mcp; print('healthy')" || exit 1

# Start MCP server
CMD ["python", "-m", "app.mcp.mcp"]
```

#### **Step 2: Create Docker Compose for Distribution**
```yaml
# docker-compose.dist.yml
version: '3.8'

services:
  cursor-automation-builder:
    image: cursor-automation-builder-mcp:latest
    container_name: cursor-automation-mcp
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      - PYTHONPATH=/app
      - MCP_LOG_LEVEL=INFO
    volumes:
      # Mount directory for workspace analysis
      - ./workspace:/workspace:ro
    healthcheck:
      test: ["CMD", "python", "-c", "from app.mcp.server import mcp; print('healthy')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 30s
```

#### **Step 3: Publish Docker Image**
```bash
# Build and publish
docker build -f Dockerfile.production -t cursor-automation-builder-mcp:latest .
docker tag cursor-automation-builder-mcp:latest your-registry/cursor-automation-builder-mcp:latest
docker push your-registry/cursor-automation-builder-mcp:latest
```

#### **Step 4: Users Run via Docker**
```bash
# Users run the container
docker run -d --name cursor-automation-mcp \
  -p 3000:3000 \
  your-registry/cursor-automation-builder-mcp:latest

# Add to their .cursor/mcp.json
{
  "mcpServers": {
    "cursor-automation-builder": {
      "url": "http://localhost:3000"
    }
  }
}
```

---

## 🔧 Easy Distribution Setup

### **Create Distribution Scripts**

#### **For Windows Users**
```batch
REM install-cursor-automation-mcp.bat
@echo off
echo 🚀 Installing Cursor Automation Builder MCP...

REM Install Python dependencies
pip install fastmcp pydantic pandas pathlib2

REM Clone repository
git clone https://github.com/yourusername/cursor-automation-builder-mcp.git
cd cursor-automation-builder-mcp

REM Test installation
python -c "from app.mcp.server import mcp; print('✅ Installation successful!')"

echo.
echo ✅ Installation complete!
echo.
echo 📝 Add this to your .cursor/mcp.json:
echo {
echo   "mcpServers": {
echo     "cursor-automation-builder": {
echo       "command": "python",
echo       "args": ["-m", "app.mcp.mcp"],
echo       "cwd": "%CD%",
echo       "env": {"PYTHONPATH": "."}
echo     }
echo   }
echo }
echo.
pause
```

#### **For macOS/Linux Users**
```bash
#!/bin/bash
# install-cursor-automation-mcp.sh

echo "🚀 Installing Cursor Automation Builder MCP..."

# Install Python dependencies
pip3 install fastmcp pydantic pandas pathlib2

# Clone repository
git clone https://github.com/yourusername/cursor-automation-builder-mcp.git
cd cursor-automation-builder-mcp

# Test installation
python3 -c "from app.mcp.server import mcp; print('✅ Installation successful!')"

echo ""
echo "✅ Installation complete!"
echo ""
echo "📝 Add this to your ~/.cursor/mcp.json:"
cat << EOF
{
  "mcpServers": {
    "cursor-automation-builder": {
      "command": "python3",
      "args": ["-m", "app.mcp.mcp"],
      "cwd": "$(pwd)",
      "env": {"PYTHONPATH": "."}
    }
  }
}
EOF
echo ""
```

---

## 📦 Complete Distribution Package

### **Create GitHub Repository**
```
cursor-automation-builder-mcp/
├── app/                          # MCP server code
├── automation-systems/           # Framework components
├── docs/                        # Documentation
├── scripts/                     # Installation scripts
│   ├── install-windows.bat
│   ├── install-macos.sh
│   └── install-linux.sh
├── docker/                      # Docker configurations
│   ├── Dockerfile.production
│   └── docker-compose.dist.yml
├── npm/                         # NPM package files
│   ├── package.json
│   └── server.js
├── mcp_requirements.txt         # Dependencies
├── README.md                    # Main documentation
├── INSTALLATION-GUIDE.md        # Step-by-step setup
└── CURSOR-INTEGRATION.md        # Cursor-specific setup
```

### **README.md for Distribution**
```markdown
# Cursor Automation System Builder MCP

Intelligent automation system builder for Cursor via Model Context Protocol (MCP).

## 🚀 Quick Install

### NPM (Recommended)
```bash
npm install -g cursor-automation-builder-mcp
```

Add to your `.cursor/mcp.json`:
```json
{
  "mcpServers": {
    "cursor-automation-builder": {
      "command": "cursor-automation-builder-mcp"
    }
  }
}
```

### Manual Installation
1. Clone this repository
2. Install dependencies: `pip install -r mcp_requirements.txt`
3. Add to your `.cursor/mcp.json` with the correct path

### Docker
```bash
docker run -d --name cursor-automation-mcp \
  -p 3000:3000 \
  cursor-automation-builder-mcp:latest
```

## 🎯 Available Tools

- `build_automation_system` - Build complete automation systems
- `analyze_workspace` - Smart workspace analysis
- `list_templates` - Browse automation templates
- And 6 more powerful automation tools!

## 📚 Documentation

See [INSTALLATION-GUIDE.md](INSTALLATION-GUIDE.md) for detailed setup instructions.

## 🤝 Contributing

Contributions welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md).
```

---

## 🎯 Testing Your Configuration

### **Update Your Current Config**
```json
# Add this block to your existing .cursor/mcp.json
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
```

### **Test the Integration**
1. Restart Cursor
2. Try: `@cursor-automation-builder analyze my workspace`
3. Try: `@cursor-automation-builder build a data processor`

---

## 🔄 Distribution Checklist

### **Before Distribution**
- [ ] Test MCP server on clean environment
- [ ] Create comprehensive documentation
- [ ] Add installation scripts for all platforms
- [ ] Set up CI/CD for automated testing
- [ ] Create example projects and tutorials

### **Distribution Methods**
- [ ] GitHub repository with releases
- [ ] NPM package for easy installation
- [ ] Docker Hub for containerized deployment
- [ ] Documentation website
- [ ] Video tutorials and examples

### **Support & Maintenance**
- [ ] Issue tracking and bug reports
- [ ] Version management and updates
- [ ] Community support channels
- [ ] Performance monitoring and optimization

---

🎯 **Your MCP server is ready for distribution and team use!**

**Recommended approach**: Start with GitHub + NPM package for widest compatibility