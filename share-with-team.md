# 🚀 Share Cursor Automation Builder with Your Team

**3 easy ways to share this MCP server with others**

---

## 🎯 **Method 1: Simple Repository Sharing** 

### **For Your Team/Company**
1. **Push to Git repository**:
   ```bash
   git add .
   git commit -m "Add Cursor Automation Builder MCP"
   git push origin main
   ```

2. **Team members clone**:
   ```bash
   git clone https://your-repo.com/cursor-automation-builder
   cd cursor-automation-builder
   pip install -r mcp_requirements.txt
   ```

3. **Team adds to their `.cursor/mcp.json`**:
   ```json
   {
     "mcpServers": {
       "cursor-automation-builder": {
         "command": "python",
         "args": ["-m", "app.mcp.mcp"],
         "cwd": "/path/to/cursor-automation-builder",
         "env": {"PYTHONPATH": "."}
       }
     }
   }
   ```

---

## 📦 **Method 2: NPM Package (Recommended)**

### **Create NPM Package**
1. **Create `package.json`**:
   ```json
   {
     "name": "your-cursor-automation-builder",
     "version": "1.0.0",
     "bin": {
       "cursor-automation-builder": "./server.js"
     },
     "dependencies": {
       "cross-spawn": "^7.0.3"
     }
   }
   ```

2. **Create `server.js`**:
   ```javascript
   #!/usr/bin/env node
   const spawn = require('cross-spawn');
   const path = require('path');
   
   const process = spawn('python', ['-m', 'app.mcp.mcp'], {
     cwd: __dirname,
     env: {...process.env, PYTHONPATH: __dirname},
     stdio: 'inherit'
   });
   ```

3. **Publish**: `npm publish`

### **Others Install**
```bash
npm install -g your-cursor-automation-builder

# Add to .cursor/mcp.json
{
  "mcpServers": {
    "cursor-automation-builder": {
      "command": "cursor-automation-builder"
    }
  }
}
```

---

## 🐳 **Method 3: Docker Container**

### **Create Container**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r mcp_requirements.txt
EXPOSE 3000
CMD ["python", "-m", "app.mcp.mcp", "--host", "0.0.0.0", "--port", "3000"]
```

### **Build and Share**
```bash
docker build -t cursor-automation-builder .
docker run -d -p 3000:3000 cursor-automation-builder
```

### **Others Use Network Server**
```json
{
  "mcpServers": {
    "cursor-automation-builder": {
      "url": "http://your-server:3000"
    }
  }
}
```

---

## 🎯 **Quick Team Setup Script**

**Create `team-install.sh`** (or `.bat` for Windows):
```bash
#!/bin/bash
echo "🚀 Installing Cursor Automation Builder..."

# Clone repository
git clone https://your-repo.com/cursor-automation-builder
cd cursor-automation-builder

# Install dependencies
pip install -r mcp_requirements.txt

# Test installation
python -c "from app.mcp.server import mcp; print('✅ Ready:', mcp.name)"

echo "📝 Add this to your .cursor/mcp.json:"
echo '{
  "mcpServers": {
    "cursor-automation-builder": {
      "command": "python",
      "args": ["-m", "app.mcp.mcp"],
      "cwd": "'$(pwd)'",
      "env": {"PYTHONPATH": "."}
    }
  }
}'
```

---

## 📚 **Documentation for Others**

### **User Guide Template**
```markdown
# Cursor Automation Builder - Team Setup

## Quick Install
1. Clone: `git clone https://your-repo.com/cursor-automation-builder`
2. Install: `pip install -r mcp_requirements.txt`
3. Add to `.cursor/mcp.json` with your local path
4. Restart Cursor
5. Test: `@cursor-automation-builder analyze my workspace`

## Available Commands
- `@cursor-automation-builder analyze workspace` - Find automation opportunities
- `@cursor-automation-builder build system` - Create automation systems
- `@cursor-automation-builder list templates` - Browse templates
- `@cursor-automation-builder help` - Get help and examples
```

---

🎯 **Choose the method that works best for your team!**

**Recommendation**: Start with Git repository sharing for team/company use, NPM package for wider distribution.