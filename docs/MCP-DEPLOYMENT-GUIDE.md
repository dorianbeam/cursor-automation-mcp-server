# 🌐 MCP Server Deployment Guide

Complete guide for deploying your Cursor Automation System Builder MCP server for remote access via `@mcp.json`.

## 🎯 Deployment Overview

Your MCP server can be deployed in multiple ways:

1. **HTTP Server** - For remote access via URL
2. **Local Command** - For local development (current setup)
3. **Docker Container** - For consistent deployment
4. **Cloud Platforms** - Railway, Render, Vercel, etc.

---

## 🌐 Option 1: HTTP Server Deployment

### **Step 1: Start HTTP Server**

```bash
# Install additional requirements
pip install fastapi uvicorn

# Start HTTP server
python -m app.mcp.http_server
```

Your server will be available at: `http://localhost:8000`

### **Step 2: Configure @mcp.json for HTTP**

```json
{
  "mcpServers": {
    "cursor-automation-builder": {
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

### **Step 3: Test HTTP Server**

```bash
# Health check
curl http://localhost:8000/health

# MCP endpoint test
curl http://localhost:8000/mcp
```

---

## ☁️ Option 2: Cloud Deployment

### **A. Railway Deployment**

1. **Connect GitHub Repository**
   - Go to [railway.app](https://railway.app)
   - Connect your GitHub account
   - Deploy from repository

2. **Automatic Configuration**
   - Railway will use `railway.json` for configuration
   - Server starts automatically with `python -m app.mcp.http_server`
   - Health checks enabled at `/health`

3. **Get Your URL**
   ```
   Your Railway URL: https://your-app-name.railway.app
   MCP Endpoint: https://your-app-name.railway.app/mcp
   ```

4. **Configure @mcp.json**
   ```json
   {
     "mcpServers": {
       "cursor-automation-builder": {
         "url": "https://your-app-name.railway.app/mcp"
       }
     }
   }
   ```

### **B. Render Deployment**

1. **Connect Repository**
   - Go to [render.com](https://render.com)
   - Create new Web Service from GitHub

2. **Configuration**
   - Uses `render.yaml` for automatic setup
   - Free tier available with limitations

3. **Get Your URL**
   ```
   Your Render URL: https://your-service-name.onrender.com
   MCP Endpoint: https://your-service-name.onrender.com/mcp
   ```

### **C. Docker Deployment**

1. **Build Docker Image**
   ```bash
   docker build -t cursor-automation-mcp .
   ```

2. **Run Container**
   ```bash
   docker run -p 8000:8000 cursor-automation-mcp
   ```

3. **Deploy to Any Container Platform**
   - Google Cloud Run
   - AWS ECS
   - Azure Container Instances
   - DigitalOcean App Platform

---

## 🏠 Option 3: Local Network Access

### **Make Local Server Accessible**

1. **Start HTTP Server on Network Interface**
   ```bash
   # Listen on all interfaces
   python -c "
   import uvicorn
   from app.mcp.http_server import app
   uvicorn.run(app, host='0.0.0.0', port=8000)
   "
   ```

2. **Find Your Local IP**
   ```bash
   # Windows
   ipconfig | findstr IPv4
   
   # Linux/Mac  
   ifconfig | grep inet
   ```

3. **Configure @mcp.json for Local Network**
   ```json
   {
     "mcpServers": {
       "cursor-automation-builder": {
         "url": "http://192.168.1.100:8000/mcp"
       }
     }
   }
   ```

---

## 🔧 Option 4: GitHub Static Hosting

For simple configuration sharing (not the full server):

1. **Create Public Repository**
   ```bash
   # Create new repo on GitHub
   # Upload your mcp.json configuration
   ```

2. **Use Raw GitHub URLs**
   ```json
   {
     "mcpServers": {
       "cursor-automation-builder": {
         "url": "https://raw.githubusercontent.com/yourusername/your-repo/main/cursor-automation-builder.mcp.json"
       }
     }
   }
   ```

**Note**: This only hosts configuration files, not the actual MCP server.

---

## 🎯 Complete Deployment Examples

### **Railway Deployment (Recommended)**

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Add HTTP MCP server deployment"
   git push origin main
   ```

2. **Deploy on Railway**
   - Visit [railway.app](https://railway.app)
   - "Deploy from GitHub repo"
   - Select your repository
   - Railway automatically detects `railway.json`

3. **Get URL and Configure**
   ```json
   {
     "mcpServers": {
       "cursor-automation-builder": {
         "url": "https://cursor-automation-system-builder-production.up.railway.app/mcp"
       }
     }
   }
   ```

### **Local Development with External Access**

1. **Install ngrok** (for temporary public URLs)
   ```bash
   # Install ngrok
   npm install -g @ngrok/ngrok
   
   # Start your HTTP server
   python -m app.mcp.http_server
   
   # In another terminal, create public tunnel
   ngrok http 8000
   ```

2. **Use ngrok URL**
   ```json
   {
     "mcpServers": {
       "cursor-automation-builder": {
         "url": "https://abc123.ngrok.io/mcp"
       }
     }
   }
   ```

---

## 🛡️ Security Considerations

### **For Production Deployment**

1. **Environment Variables**
   ```bash
   # Set secure environment variables
   export MCP_API_KEY="your-secure-key"
   export ALLOWED_ORIGINS="https://yourdomain.com"
   ```

2. **Update HTTP Server for Security**
   ```python
   # Add authentication middleware
   # Restrict CORS origins
   # Add rate limiting
   ```

3. **HTTPS Only**
   ```json
   {
     "mcpServers": {
       "cursor-automation-builder": {
         "url": "https://your-domain.com/mcp",
         "headers": {
           "Authorization": "Bearer your-api-key"
         }
       }
     }
   }
   ```

---

## 🧪 Testing Your Deployment

### **1. Health Check**
```bash
curl https://your-deployed-url.com/health
```

### **2. MCP Endpoint Test**
```bash
curl https://your-deployed-url.com/mcp
```

### **3. Tool Availability**
```bash
curl https://your-deployed-url.com/mcp/tools
```

### **4. Full Integration Test**
```json
// Test with MCP client
{
  "method": "tools/list",
  "params": {}
}
```

---

## 🚀 Recommended Deployment Flow

### **For Personal Use**
1. ✅ Start with **Railway** (free tier, easy setup)
2. ✅ Use **Docker** for local consistent deployment
3. ✅ **ngrok** for temporary external access

### **For Team Use**
1. ✅ **Railway Pro** or **Render** for reliable hosting
2. ✅ **Docker** deployment on your cloud provider
3. ✅ Add authentication and security measures

### **For Production Use**
1. ✅ **Container deployment** (Google Cloud Run, AWS ECS)
2. ✅ **Custom domain** with SSL certificate
3. ✅ **API authentication** and rate limiting
4. ✅ **Monitoring** and logging

---

## 📁 Files Created for Deployment

```
├── app/mcp/http_server.py      # HTTP server implementation
├── Dockerfile                  # Container deployment
├── railway.json               # Railway platform config
├── render.yaml                # Render platform config
├── mcp_requirements.txt       # Updated with HTTP deps
└── MCP-DEPLOYMENT-GUIDE.md    # This guide
```

---

## 🎯 Quick Start Commands

### **1. Local HTTP Server**
```bash
pip install fastapi uvicorn
python -m app.mcp.http_server
# Use: http://localhost:8000/mcp
```

### **2. Railway Deployment**
```bash
git push origin main
# Deploy via Railway dashboard
# Use: https://your-app.railway.app/mcp
```

### **3. Docker Deployment**  
```bash
docker build -t cursor-automation-mcp .
docker run -p 8000:8000 cursor-automation-mcp
# Use: http://localhost:8000/mcp
```

### **4. Configure Any MCP Client**
```json
{
  "mcpServers": {
    "cursor-automation-builder": {
      "url": "YOUR_DEPLOYED_URL/mcp"
    }
  }
}
```

---

🎯 **Your MCP server is now deployable to any cloud platform and accessible via HTTP URLs!**

**Next Steps:**
1. Choose your deployment method
2. Deploy and get your URL  
3. Update `@mcp.json` with your URL
4. Test with your MCP client
5. Start building automation systems remotely!
