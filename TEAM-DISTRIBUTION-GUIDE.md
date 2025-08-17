# 👥 Team Distribution Guide - Share Your MCP Server

**How to make your Cursor Automation System Builder available to others**

---

## 🎯 **For Your Team/Organization**

### **Method 1: Git Repository Sharing (Simple)**

#### **Create Shared Repository**
```bash
# Create a new repository for your team
git init cursor-automation-builder-mcp
cd cursor-automation-builder-mcp

# Copy your framework
cp -r C:\Users\dsber\Code\Cursor-Automation-System-Builder\app .
cp -r C:\Users\dsber\Code\Cursor-Automation-System-Builder\automation-systems .
cp C:\Users\dsber\Code\Cursor-Automation-System-Builder\mcp_requirements.txt .
cp C:\Users\dsber\Code\Cursor-Automation-System-Builder\*.md .

# Push to your team's Git server
git add .
git commit -m "Add Cursor Automation Builder MCP Server"
git remote add origin https://your-git-server.com/team/cursor-automation-builder-mcp
git push -u origin main
```

#### **Team Installation Instructions**
Create `TEAM-INSTALL.md`:
```markdown
# Team Installation - Cursor Automation Builder

## Quick Setup
1. Clone the repository:
   ```bash
   git clone https://your-git-server.com/team/cursor-automation-builder-mcp
   cd cursor-automation-builder-mcp
   ```

2. Install dependencies:
   ```bash
   pip install -r mcp_requirements.txt
   ```

3. Add to your `.cursor/mcp.json`:
   ```json
   {
     "mcpServers": {
       "cursor-automation-builder": {
         "command": "python",
         "args": ["-m", "app.mcp.mcp"],
         "cwd": "/full/path/to/cursor-automation-builder-mcp",
         "env": {"PYTHONPATH": "."}
       }
     }
   }
   ```

4. Restart Cursor
5. Test with: `@cursor-automation-builder analyze my workspace`
```

### **Method 2: Network Server (Advanced)**

#### **Set up Central MCP Server**
```python
# File: network_mcp_server.py
import uvicorn
from app.mcp.server import mcp

# Configure for network access
mcp.configure_network_server(
    host="0.0.0.0",  # Allow external connections
    port=3000,
    cors_origins=["*"]  # Configure CORS as needed
)

if __name__ == "__main__":
    uvicorn.run(
        "app.mcp.server:mcp",
        host="0.0.0.0",
        port=3000,
        reload=False
    )
```

#### **Team Uses Network Server**
```json
# Team members add this to their .cursor/mcp.json
{
  "mcpServers": {
    "cursor-automation-builder": {
      "url": "http://your-server.company.com:3000"
    }
  }
}
```

---

## 🌐 **For Public Distribution**

### **Method 3: NPM Package (Recommended)**

#### **Create NPM Package Structure**
```
cursor-automation-builder-mcp/
├── package.json
├── server.js                 # Node.js wrapper
├── install.js               # Post-install script  
├── app/                     # Your Python MCP code
├── automation-systems/      # Framework components
├── mcp_requirements.txt     # Python dependencies
├── README.md               # Documentation
└── INSTALL-GUIDE.md        # Setup instructions
```

#### **package.json**
```json
{
  "name": "cursor-automation-builder-mcp",
  "version": "1.0.0",
  "description": "Intelligent automation system builder for Cursor via MCP",
  "main": "server.js",
  "bin": {
    "cursor-automation-builder-mcp": "./server.js"
  },
  "scripts": {
    "postinstall": "node install.js",
    "start": "node server.js",
    "test": "python -c 'from app.mcp.server import mcp; print(\"✅ MCP server ready:\", mcp.name)'"
  },
  "keywords": ["mcp", "cursor", "automation", "ai", "code-generation"],
  "author": "Your Name <your.email@example.com>",
  "license": "MIT",
  "repository": {
    "type": "git",
    "url": "https://github.com/yourusername/cursor-automation-builder-mcp"
  },
  "dependencies": {
    "cross-spawn": "^7.0.3",
    "chalk": "^4.1.2"
  },
  "engines": {
    "node": ">=14.0.0"
  }
}
```

#### **server.js (Node.js Wrapper)**
```javascript
#!/usr/bin/env node
const spawn = require('cross-spawn');
const path = require('path');
const chalk = require('chalk');

console.log(chalk.blue('🚀 Starting Cursor Automation Builder MCP Server...'));

// Get package directory
const packageDir = __dirname;

// Start Python MCP server
const pythonProcess = spawn('python', ['-m', 'app.mcp.mcp'], {
  cwd: packageDir,
  env: {
    ...process.env,
    PYTHONPATH: packageDir
  },
  stdio: 'inherit'
});

// Handle process termination
process.on('SIGINT', () => {
  console.log(chalk.yellow('\n🛑 Shutting down MCP server...'));
  pythonProcess.kill('SIGINT');
});

process.on('SIGTERM', () => {
  pythonProcess.kill('SIGTERM');
});

pythonProcess.on('exit', (code) => {
  if (code !== 0) {
    console.error(chalk.red(`❌ MCP server exited with code ${code}`));
    process.exit(code);
  }
});
```

#### **install.js (Post-Install Script)**
```javascript
const { spawn } = require('cross-spawn');
const chalk = require('chalk');
const path = require('path');
const fs = require('fs');

console.log(chalk.blue('📦 Installing Cursor Automation Builder MCP...'));

// Check if Python is available
const pythonCheck = spawn.sync('python', ['--version'], { stdio: 'pipe' });
if (pythonCheck.error) {
  console.error(chalk.red('❌ Python not found. Please install Python 3.8+ first.'));
  process.exit(1);
}

console.log(chalk.green('✅ Python found'));

// Install Python dependencies
console.log(chalk.blue('📦 Installing Python dependencies...'));
const pipInstall = spawn.sync('pip', ['install', '-r', 'mcp_requirements.txt'], {
  stdio: 'inherit',
  cwd: __dirname
});

if (pipInstall.status !== 0) {
  console.error(chalk.red('❌ Failed to install Python dependencies'));
  console.log(chalk.yellow('💡 Try: pip install fastmcp pydantic pandas pathlib2'));
  process.exit(1);
}

console.log(chalk.green('✅ Python dependencies installed'));

// Test MCP server
console.log(chalk.blue('🧪 Testing MCP server...'));
const serverTest = spawn.sync('python', ['-c', 'from app.mcp.server import mcp; print("MCP server ready:", mcp.name)'], {
  cwd: __dirname,
  env: {
    ...process.env,
    PYTHONPATH: __dirname
  }
});

if (serverTest.status !== 0) {
  console.error(chalk.red('❌ MCP server test failed'));
  process.exit(1);
}

console.log(chalk.green('✅ MCP server test passed'));

// Show configuration instructions
console.log(chalk.blue('\n📝 Configuration Instructions:'));
console.log(chalk.white('Add this to your .cursor/mcp.json:'));
console.log(chalk.gray('```json'));
console.log(chalk.white(JSON.stringify({
  "mcpServers": {
    "cursor-automation-builder": {
      "command": "cursor-automation-builder-mcp"
    }
  }
}, null, 2)));
console.log(chalk.gray('```'));

console.log(chalk.green('\n🎉 Installation complete!'));
console.log(chalk.blue('🚀 Restart Cursor and test with: @cursor-automation-builder analyze my workspace'));
```

#### **Publish to NPM**
```bash
# Login to NPM
npm login

# Publish package
npm publish

# Users can then install with:
# npm install -g cursor-automation-builder-mcp
```

### **Method 4: Docker Hub Distribution**

#### **Create Production Dockerfile**
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY mcp_requirements.txt .
RUN pip install --no-cache-dir -r mcp_requirements.txt

# Copy application code
COPY app/ ./app/
COPY automation-systems/ ./automation-systems/

# Set environment variables
ENV PYTHONPATH=/app
ENV MCP_LOG_LEVEL=INFO

# Expose MCP port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
  CMD python -c "from app.mcp.server import mcp; print('healthy')" || exit 1

# Start MCP server
CMD ["python", "-m", "app.mcp.mcp", "--host", "0.0.0.0", "--port", "3000"]
```

#### **Build and Publish Docker Image**
```bash
# Build image
docker build -t cursor-automation-builder-mcp:latest .

# Tag for Docker Hub
docker tag cursor-automation-builder-mcp:latest yourusername/cursor-automation-builder-mcp:latest

# Push to Docker Hub
docker push yourusername/cursor-automation-builder-mcp:latest
```

#### **Users Run with Docker**
```bash
# Users run the container
docker run -d \
  --name cursor-automation-mcp \
  -p 3000:3000 \
  --restart unless-stopped \
  yourusername/cursor-automation-builder-mcp:latest

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

## 🎯 **Quick Distribution Options**

### **Option A: Share Your Current Setup**
1. **Zip your project directory**
2. **Include setup instructions**:
   ```
   1. Extract to any folder
   2. Install dependencies: pip install -r mcp_requirements.txt
   3. Add to .cursor/mcp.json with correct path
   4. Restart Cursor
   ```

### **Option B: GitHub Release**
1. **Push to GitHub**
2. **Create Release** with installation instructions
3. **Include pre-built packages** for different platforms

### **Option C: Company Internal Package**
1. **Use your company's package registry**
2. **Follow internal deployment procedures**
3. **Add to company documentation**

---

## 📚 **Documentation Templates**

### **README.md for Public Distribution**
```markdown
# Cursor Automation System Builder MCP

🤖 Intelligent automation system builder for Cursor via Model Context Protocol (MCP).

## ✨ Features

- **Build Complete Systems**: Create automation systems from natural language
- **Smart Workspace Analysis**: AI-powered detection of automation opportunities  
- **Template Library**: 5+ proven templates with auto-generation
- **Learning Integration**: Guided tutorials with hands-on building
- **Meta-Optimization**: Continuous system improvement

## 🚀 Quick Install

### NPM (Recommended)
```bash
npm install -g cursor-automation-builder-mcp
```

### Manual Install
```bash
git clone https://github.com/yourusername/cursor-automation-builder-mcp
cd cursor-automation-builder-mcp
pip install -r mcp_requirements.txt
```

## ⚙️ Configuration

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

## 🎯 Usage

```
@cursor-automation-builder analyze my workspace
@cursor-automation-builder build a data processing system
@cursor-automation-builder list available templates
```

## 🛠️ Available Tools

- `build_automation_system` - Build complete automation systems
- `analyze_workspace` - Smart workspace analysis with suggestions
- `list_templates` - Browse available automation templates
- `build_from_template` - Fast template-based building
- And 5 more powerful automation tools!

## 📖 Documentation

- [Installation Guide](docs/INSTALLATION.md)
- [Usage Examples](docs/EXAMPLES.md)
- [Template Creation](docs/TEMPLATES.md)
- [API Reference](docs/API.md)

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.
```

---

## 🎯 **Distribution Checklist**

### **Before Release**
- [ ] Test on clean environment
- [ ] Create comprehensive documentation
- [ ] Add example projects and tutorials
- [ ] Set up automated testing
- [ ] Security review and dependency audit

### **Distribution Setup**
- [ ] Choose distribution method (NPM recommended)
- [ ] Create installation scripts for all platforms
- [ ] Set up CI/CD pipeline
- [ ] Create GitHub repository with releases
- [ ] Add community support channels

### **Post-Release**
- [ ] Monitor usage and feedback
- [ ] Respond to issues and bug reports
- [ ] Regular updates and improvements
- [ ] Community building and support

---

🎯 **Your MCP server is ready for team and public distribution!**

**Recommended approach**: Start with NPM package for easiest installation and widest compatibility.