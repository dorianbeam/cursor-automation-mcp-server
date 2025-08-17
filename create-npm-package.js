#!/usr/bin/env node

/**
 * Script to create NPM package for distributing Cursor Automation Builder MCP
 */

const fs = require('fs');
const path = require('path');

console.log('🚀 Creating NPM package for Cursor Automation Builder MCP...');

// Create package.json
const packageJson = {
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
    "test": "python -c \"from app.mcp.server import mcp; print('✅ MCP server ready:', mcp.name)\""
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
};

// Create server.js wrapper
const serverJs = `#!/usr/bin/env node
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
  console.log(chalk.yellow('\\n🛑 Shutting down MCP server...'));
  pythonProcess.kill('SIGINT');
});

process.on('SIGTERM', () => {
  pythonProcess.kill('SIGTERM');
});

pythonProcess.on('exit', (code) => {
  if (code !== 0) {
    console.error(chalk.red(\`❌ MCP server exited with code \${code}\`));
    process.exit(code);
  }
});
`;

// Create install.js post-install script
const installJs = `const { spawn } = require('cross-spawn');
const chalk = require('chalk');

console.log(chalk.blue('📦 Installing Cursor Automation Builder MCP...'));

// Check Python
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

console.log(chalk.green('✅ Installation complete!'));
console.log(chalk.blue('\\n📝 Add this to your .cursor/mcp.json:'));
console.log(chalk.white(JSON.stringify({
  "mcpServers": {
    "cursor-automation-builder": {
      "command": "cursor-automation-builder-mcp"
    }
  }
}, null, 2)));
`;

// Create README
const readmeContent = `# Cursor Automation System Builder MCP

🤖 Intelligent automation system builder for Cursor via Model Context Protocol (MCP).

## 🚀 Quick Install

\`\`\`bash
npm install -g cursor-automation-builder-mcp
\`\`\`

## ⚙️ Configuration

Add to your \`.cursor/mcp.json\`:

\`\`\`json
{
  "mcpServers": {
    "cursor-automation-builder": {
      "command": "cursor-automation-builder-mcp"
    }
  }
}
\`\`\`

## 🎯 Usage

\`\`\`
@cursor-automation-builder analyze my workspace
@cursor-automation-builder build a data processing system
@cursor-automation-builder list available templates
\`\`\`

## 🛠️ Available Tools

- \`build_automation_system\` - Build complete automation systems
- \`analyze_workspace\` - Smart workspace analysis
- \`list_templates\` - Browse automation templates
- And 6 more powerful tools!

## 📖 Documentation

See the full documentation at: [GitHub Repository]

## 📄 License

MIT License
`;

// Write files
console.log('📝 Writing package files...');

fs.writeFileSync('package.json', JSON.stringify(packageJson, null, 2));
console.log('✅ Created package.json');

fs.writeFileSync('server.js', serverJs);
fs.chmodSync('server.js', '755');
console.log('✅ Created server.js');

fs.writeFileSync('install.js', installJs);
console.log('✅ Created install.js');

fs.writeFileSync('README.md', readmeContent);
console.log('✅ Created README.md');

console.log('\n🎉 NPM package structure created!');
console.log('\n📦 To publish:');
console.log('1. npm login');
console.log('2. npm publish');
console.log('\n👥 Others can then install with:');
console.log('npm install -g cursor-automation-builder-mcp');