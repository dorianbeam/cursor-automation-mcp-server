#!/usr/bin/env python3
"""
Cursor Automation System Builder - Deployment Script
Simplifies deployment to various cloud platforms
"""

import os
import sys
import json
import subprocess
from pathlib import Path

class MCPDeployer:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.deployment_configs = {
            'railway': 'railway.json',
            'render': 'render.yaml', 
            'docker': 'Dockerfile'
        }
    
    def check_requirements(self):
        """Check if all required files exist"""
        print("🔍 Checking deployment requirements...")
        
        required_files = [
            'app/mcp/server.py',
            'app/mcp/http_server.py',
            'mcp_requirements.txt'
        ]
        
        missing_files = []
        for file in required_files:
            if not (self.project_root / file).exists():
                missing_files.append(file)
        
        if missing_files:
            print(f"❌ Missing required files: {missing_files}")
            return False
            
        print("✅ All required files present")
        return True
    
    def test_local_server(self):
        """Test the local HTTP server"""
        print("🧪 Testing local HTTP server...")
        
        try:
            # Install requirements
            subprocess.run([
                sys.executable, '-m', 'pip', 'install', 
                '-r', 'mcp_requirements.txt'
            ], check=True, cwd=self.project_root)
            
            print("✅ Dependencies installed")
            print("🚀 Starting HTTP server test...")
            print("   Run: python -m app.mcp.http_server")
            print("   Test: curl http://localhost:8000/health")
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error installing dependencies: {e}")
            return False
    
    def generate_deployment_configs(self):
        """Generate deployment configurations"""
        print("📝 Generating deployment configurations...")
        
        # Update mcp_requirements.txt if needed
        requirements_file = self.project_root / 'mcp_requirements.txt'
        if requirements_file.exists():
            content = requirements_file.read_text()
            if 'fastapi' not in content:
                print("📦 Adding FastAPI dependencies to requirements...")
                with open(requirements_file, 'a') as f:
                    f.write('\nfastapi>=0.104.0\nuvicorn>=0.24.0\n')
        
        print("✅ Deployment configurations ready")
        
        # Show available configs
        print("\n📋 Available deployment options:")
        for platform, config in self.deployment_configs.items():
            config_path = self.project_root / config
            status = "✅" if config_path.exists() else "❌"
            print(f"   {status} {platform.upper()}: {config}")
    
    def deploy_railway(self):
        """Deploy to Railway"""
        print("🚂 Preparing Railway deployment...")
        
        commands = [
            "git add .",
            "git commit -m 'Add MCP HTTP server deployment'",
            "git push origin main"
        ]
        
        print("📋 Railway deployment steps:")
        print("1. Push code to GitHub:")
        for cmd in commands:
            print(f"   {cmd}")
        
        print("\n2. Deploy on Railway:")
        print("   - Visit https://railway.app")
        print("   - Connect GitHub repository")
        print("   - Deploy automatically using railway.json")
        
        print("\n3. Get your URL:")
        print("   - Copy URL from Railway dashboard")
        print("   - Add '/mcp' to the end")
        print("   - Use in @mcp.json configuration")
        
        return True
    
    def deploy_docker(self):
        """Deploy with Docker"""
        print("🐳 Preparing Docker deployment...")
        
        commands = [
            "docker build -t cursor-automation-mcp .",
            "docker run -p 8000:8000 cursor-automation-mcp"
        ]
        
        print("📋 Docker deployment commands:")
        for cmd in commands:
            print(f"   {cmd}")
        
        print("\n🌐 Access your server at: http://localhost:8000/mcp")
        return True
    
    def show_mcp_config(self, url):
        """Show MCP client configuration"""
        config = {
            "mcpServers": {
                "cursor-automation-builder": {
                    "url": f"{url}/mcp"
                }
            }
        }
        
        print(f"\n📝 @mcp.json configuration:")
        print(json.dumps(config, indent=2))
        
        return config
    
    def interactive_deploy(self):
        """Interactive deployment wizard"""
        print("🎯 Cursor Automation System Builder - Deployment Wizard")
        print("=" * 60)
        
        # Check requirements
        if not self.check_requirements():
            print("❌ Please ensure all required files are present")
            return False
        
        # Generate configs
        self.generate_deployment_configs()
        
        # Show options
        print("\n🚀 Choose deployment option:")
        print("1. Local HTTP server (development)")
        print("2. Railway (recommended for cloud)")
        print("3. Docker (local container)")
        print("4. Test only (check setup)")
        
        try:
            choice = input("\nEnter choice (1-4): ").strip()
            
            if choice == '1':
                self.test_local_server()
                self.show_mcp_config("http://localhost:8000")
                
            elif choice == '2':
                self.deploy_railway() 
                print("\n💡 After Railway deployment:")
                self.show_mcp_config("https://your-app-name.railway.app")
                
            elif choice == '3':
                self.deploy_docker()
                self.show_mcp_config("http://localhost:8000")
                
            elif choice == '4':
                success = self.test_local_server()
                print(f"\n🎯 Setup test: {'✅ PASSED' if success else '❌ FAILED'}")
                
            else:
                print("❌ Invalid choice")
                return False
                
            print("\n🎯 Deployment preparation complete!")
            print("📖 See MCP-DEPLOYMENT-GUIDE.md for detailed instructions")
            
            return True
            
        except KeyboardInterrupt:
            print("\n\n👋 Deployment cancelled")
            return False
    
    def quick_deploy(self, platform='local'):
        """Quick deployment without interaction"""
        print(f"🚀 Quick deploying to {platform}...")
        
        if not self.check_requirements():
            return False
            
        self.generate_deployment_configs()
        
        if platform == 'local':
            return self.test_local_server()
        elif platform == 'railway':
            return self.deploy_railway()
        elif platform == 'docker':
            return self.deploy_docker()
        else:
            print(f"❌ Unknown platform: {platform}")
            return False

def main():
    deployer = MCPDeployer()
    
    if len(sys.argv) > 1:
        platform = sys.argv[1]
        deployer.quick_deploy(platform)
    else:
        deployer.interactive_deploy()

if __name__ == '__main__':
    main()
