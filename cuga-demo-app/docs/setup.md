# CUGA Demo Application - Setup Guide

This guide will help you set up and configure the CUGA demo application.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.12 or higher**
- **pip** or **uv** (recommended package manager)
- **Git** (for cloning repositories)
- **Docker or Podman** (optional, for sandbox execution)
- **Node.js and npm** (optional, for MCP servers)

## Installation Steps

### 1. Clone or Download the Project

```bash
cd cuga-demo-app
```

### 2. Set Up Python Environment

#### Using uv (Recommended)

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

#### Using pip

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your preferred editor
nano .env  # or vim, code, etc.
```

### 4. Choose Your LLM Provider

Edit the `.env` file and configure one of the following providers:

#### Option A: OpenAI

```env
OPENAI_API_KEY=sk-your-api-key-here
AGENT_SETTING_CONFIG="settings.openai.toml"
MODEL_NAME=gpt-4o
```

#### Option B: IBM WatsonX

```env
WATSONX_API_KEY=your-watsonx-api-key
WATSONX_PROJECT_ID=your-project-id
WATSONX_URL=https://us-south.ml.cloud.ibm.com
AGENT_SETTING_CONFIG="settings.watsonx.toml"
```

#### Option C: Azure OpenAI

```env
AZURE_OPENAI_API_KEY=your-azure-api-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
OPENAI_API_VERSION=2024-08-01-preview
AGENT_SETTING_CONFIG="settings.azure.toml"
```

#### Option D: OpenRouter

```env
OPENROUTER_API_KEY=your-openrouter-api-key
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
AGENT_SETTING_CONFIG="settings.openrouter.toml"
MODEL_NAME=openai/gpt-4o
```

### 5. Configure CUGA Settings

Edit `config/settings.toml` to customize:

```toml
[features]
# Choose reasoning mode: fast, balanced, accurate
cuga_mode = "balanced"

# Enable experimental features
enable_memory = false
enable_save_reuse = false

[advanced_features]
# Choose task mode: api, web, hybrid
mode = "api"

# Enable sandbox for secure code execution
use_sandbox = false
```

### 6. Verify Installation

```bash
# Check setup
python src/main.py check-setup

# Run basic examples
python src/examples/basic_usage.py

# Test API agent
python src/agents/api_agent.py

# Test custom tools
python src/tools/custom_tools.py
```

## Optional: Advanced Setup

### Enable Sandbox Execution

For secure code execution using Docker/Podman:

1. **Install Docker Desktop or Rancher Desktop**
   - Download from [docker.com](https://www.docker.com/) or [rancherdesktop.io](https://rancherdesktop.io/)

2. **Enable sandbox in configuration**
   ```toml
   [advanced_features]
   use_sandbox = true
   sandbox_runtime = "docker"  # or "podman"
   ```

3. **Test sandbox**
   ```bash
   python src/main.py run --task "execute python code safely"
   ```

### Enable Memory Features

For agents that learn from past executions:

1. **Install memory dependencies**
   ```bash
   pip install redis chromadb
   ```

2. **Enable memory in configuration**
   ```toml
   [features]
   enable_memory = true
   
   [memory]
   memory_backend = "local"  # or "redis", "chromadb"
   memory_path = "./data/memory"
   ```

### Set Up Web/Hybrid Mode

For browser-based interactions:

1. **Install Playwright**
   ```bash
   pip install playwright
   playwright install chromium
   ```

2. **Configure web mode**
   ```toml
   [advanced_features]
   mode = "web"  # or "hybrid"
   
   [demo_mode]
   start_url = "https://your-demo-site.com"
   ```

### Configure Custom Tools

#### OpenAPI Tools

1. Add your OpenAPI spec to `src/tools/openapi_specs/`
2. Register in `config/tools/mcp_servers.yaml`:
   ```yaml
   openapi_tools:
     - name: "my_api"
       description: "My custom API"
       spec_path: "src/tools/openapi_specs/my_api.yaml"
       enabled: true
   ```

#### MCP Servers

1. Install MCP server (example):
   ```bash
   npm install -g @modelcontextprotocol/server-filesystem
   ```

2. Register in `config/tools/mcp_servers.yaml`:
   ```yaml
   mcp_servers:
     - name: "my_mcp"
       description: "My MCP server"
       command: "npx"
       args:
         - "-y"
         - "@modelcontextprotocol/server-filesystem"
         - "/path/to/directory"
       enabled: true
   ```

#### LangChain Tools

1. Create your tool in `src/tools/custom_tools.py`
2. Register in `config/tools/mcp_servers.yaml`:
   ```yaml
   langchain_tools:
     - name: "my_tool"
       module: "src.tools.custom_tools"
       class: "MyCustomTool"
       enabled: true
   ```

## Troubleshooting

### Common Issues

#### Import Errors

```bash
# Ensure you're in the virtual environment
source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

#### API Key Issues

```bash
# Verify your .env file exists
ls -la .env

# Check environment variables are loaded
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('OPENAI_API_KEY'))"
```

#### Configuration Not Found

```bash
# Verify config files exist
ls -la config/settings.toml
ls -la config/modes/

# Check file paths in .env
cat .env | grep AGENT_SETTING_CONFIG
```

### Getting Help

- **GitHub Issues**: [Report issues](https://github.com/cuga-project/cuga-agent/issues)
- **Discord**: [Join community](https://discord.gg/aH6rAEEW)
- **Documentation**: [Official docs](https://docs.cuga.dev)

## Next Steps

Once setup is complete:

1. **Run Examples**: `python src/examples/basic_usage.py`
2. **Try Interactive Mode**: `python src/main.py interactive`
3. **Explore Agents**: Check out `src/agents/` directory
4. **Read Usage Guide**: See `docs/usage.md`
5. **View Examples**: See `docs/examples.md`

## Updating

To update the demo application:

```bash
# Pull latest changes (if using git)
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Verify setup
python src/main.py check-setup
```

## Uninstallation

To remove the demo application:

```bash
# Deactivate virtual environment
deactivate

# Remove virtual environment
rm -rf .venv

# Remove data and logs (optional)
rm -rf data/ logs/

# Remove the entire directory
cd ..
rm -rf cuga-demo-app