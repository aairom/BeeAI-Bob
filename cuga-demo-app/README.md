# CUGA Demo Application

A comprehensive demonstration application showcasing the implementation and usage of CUGA (Collaborative Universal Generative Agent).

## Overview

This application demonstrates how to integrate and use CUGA for building intelligent agents that can:
- Execute API calls and web interactions
- Handle complex multi-step tasks
- Switch between different reasoning modes (fast/balanced/accurate)
- Integrate custom tools via OpenAPI, MCP, and LangChain
- Save and reuse successful execution patterns

## Features Demonstrated

### 1. **Basic CUGA Integration**
- Setting up CUGA with different LLM providers (Ollama, OpenAI, watsonx, Azure, OpenRouter)
- **NEW: Local LLM support with Ollama** - Run completely free and private!
- Configuring agent modes and reasoning strategies
- Managing environment variables and configurations

### 2. **Task Execution Modes**
- **API Mode**: Execute API-focused tasks
- **Web Mode**: Browser-based interactions
- **Hybrid Mode**: Combined API and web operations

### 3. **Custom Tool Integration**
- OpenAPI specification tools
- MCP (Model Context Protocol) servers
- LangChain Python functions

### 4. **Advanced Features**
- Memory-enabled agents for learning from past executions
- Save & Reuse patterns for faster repeated tasks
- Secure code sandbox execution with Docker/Podman

## Project Structure

```
cuga-demo-app/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── .env.example                       # Environment variables template
├── config/
│   ├── settings.toml                  # Main CUGA configuration
│   ├── modes/
│   │   ├── fast.toml                  # Fast reasoning mode
│   │   ├── balanced.toml              # Balanced mode (default)
│   │   └── accurate.toml              # Accurate mode
│   └── tools/
│       └── mcp_servers.yaml           # Custom tools configuration
├── src/
│   ├── __init__.py
│   ├── main.py                        # Main application entry point
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── api_agent.py               # API-focused agent
│   │   ├── web_agent.py               # Web interaction agent
│   │   └── hybrid_agent.py            # Hybrid mode agent
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── custom_tools.py            # Custom LangChain tools
│   │   └── openapi_specs/
│   │       └── sample_api.yaml        # Sample OpenAPI specification
│   └── examples/
│       ├── __init__.py
│       ├── basic_usage.py             # Basic CUGA usage examples
│       ├── advanced_usage.py          # Advanced features demo
│       └── tool_integration.py        # Custom tool integration examples
├── tests/
│   ├── __init__.py
│   ├── test_agents.py                 # Agent tests
│   └── test_tools.py                  # Tool integration tests
└── docs/
    ├── setup.md                       # Setup instructions
    ├── usage.md                       # Usage guide
    └── examples.md                    # Example scenarios
```

## Quick Start

### Option A: Using Ollama (Recommended - Free & Local!)

**Perfect for getting started without API costs!**

1. **Install Ollama:**
   ```bash
   # Visit https://ollama.ai or use:
   # macOS: brew install ollama
   # Linux: curl -fsSL https://ollama.com/install.sh | sh
   ```

2. **Pull a model:**
   ```bash
   ollama pull llama3.2
   # Or try: phi3, mistral, codellama
   ```

3. **Setup the demo app:**
   ```bash
   cd cuga-demo-app
   cp .env.example .env
   ```

4. **Configure for Ollama (edit .env):**
   ```env
   OPENAI_API_KEY=ollama
   OPENAI_BASE_URL=http://localhost:11434/v1
   AGENT_SETTING_CONFIG="settings.openai.toml"
   MODEL_NAME=llama3.2
   ```

5. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

6. **Run it:**
   ```bash
   python src/main.py check-setup
   python src/main.py interactive
   ```

### Option B: Using Cloud Providers (OpenAI, watsonx, etc.)

1. **Clone and setup:**
   ```bash
   cd cuga-demo-app
   cp .env.example .env
   # Edit .env with your API keys
   ```

2. **Install dependencies:**
   ```bash
   # Using uv (recommended)
   uv sync
   
   # Or using pip
   pip install -r requirements.txt
   ```

3. **Configure CUGA:**
   Edit `config/settings.toml` to set your preferred mode and features.

### Prerequisites

- Python 3.12+
- uv (recommended) or pip
- **For Ollama**: Ollama installed locally (free!)
- **For Cloud**: API keys for your chosen LLM provider
- Docker/Podman (optional, for sandbox execution)

### Running Examples

#### Basic Usage
```bash
python src/examples/basic_usage.py
```

#### API Agent
```bash
python src/agents/api_agent.py
```

#### Web Agent (requires browser extension)
```bash
python src/agents/web_agent.py
```

#### Hybrid Agent
```bash
python src/agents/hybrid_agent.py
```

## Configuration

### LLM Provider Setup

#### Ollama (Local - Recommended)
```env
OPENAI_API_KEY=ollama
OPENAI_BASE_URL=http://localhost:11434/v1
AGENT_SETTING_CONFIG="settings.openai.toml"
MODEL_NAME=llama3.2
```

**Benefits:**
- ✅ Completely free
- ✅ 100% private - data never leaves your machine
- ✅ Works offline
- ✅ No API rate limits
- ✅ Multiple models available (llama3.2, mistral, phi3, codellama, etc.)

**See [OLLAMA_SETUP.md](docs/OLLAMA_SETUP.md) for detailed instructions.**

#### OpenAI
```env
OPENAI_API_KEY=your-api-key
AGENT_SETTING_CONFIG="settings.openai.toml"
MODEL_NAME=gpt-4o
```

#### IBM watsonx
```env
WATSONX_API_KEY=your-api-key
WATSONX_PROJECT_ID=your-project-id
WATSONX_URL=https://us-south.ml.cloud.ibm.com
AGENT_SETTING_CONFIG="settings.watsonx.toml"
```

#### Azure OpenAI
```env
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_ENDPOINT=your-endpoint
OPENAI_API_VERSION=2024-08-01-preview
AGENT_SETTING_CONFIG="settings.azure.toml"
```

#### OpenRouter
```env
OPENROUTER_API_KEY=your-api-key
AGENT_SETTING_CONFIG="settings.openrouter.toml"
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
```

### Reasoning Modes

Edit `config/settings.toml`:
```toml
[features]
cuga_mode = "balanced"  # Options: fast, balanced, accurate, custom
```

### Task Modes

```toml
[advanced_features]
mode = 'api'  # Options: api, web, hybrid
```

## Example Use Cases

### 1. CRM Operations
```python
# Get top accounts by revenue
task = "get top 5 accounts by revenue from digital sales"
result = agent.execute(task)
```

### 2. Web Automation
```python
# Navigate and extract data
task = "go to the dashboard and extract the latest sales figures"
result = web_agent.execute(task)
```

### 3. Hybrid Operations
```python
# Combine API and web operations
task = "get top account by revenue from API, then add it to current page"
result = hybrid_agent.execute(task)
```

### 4. Custom Tool Usage
```python
# Use custom tools
task = "analyze customer sentiment using my custom NLP tool"
result = agent.execute(task)
```

## Advanced Features

### Memory-Enabled Agents
```bash
# Enable memory in config/settings.toml
enable_memory = true

# Run with memory
python src/examples/advanced_usage.py --memory
```

### Save & Reuse
```toml
[features]
cuga_mode = "save_reuse_fast"
```

### Secure Sandbox
```bash
# Run with Docker/Podman sandbox
python src/main.py --sandbox
```

## Testing

```bash
# Run all tests
pytest tests/

# Run specific test
pytest tests/test_agents.py

# Run with coverage
pytest --cov=src tests/
```

## Benchmarks

CUGA achieves state-of-the-art performance:
- 🥇 #1 on AppWorld (750 real-world tasks across 457 APIs)
- 🥈 Top-tier on WebArena (complex autonomous web agent benchmark)

## Resources

### CUGA Resources
- [CUGA GitHub Repository](https://github.com/cuga-project/cuga-agent)
- [Official Documentation](https://docs.cuga.dev)
- [Discord Community](https://discord.gg/aH6rAEEW)
- [Try CUGA Live](https://huggingface.co/spaces/ibm-research/cuga-agent)

### Ollama Resources
- [Ollama Website](https://ollama.ai)
- [Ollama GitHub](https://github.com/ollama/ollama)
- [Ollama Model Library](https://ollama.ai/library)
- [OpenAI API Compatibility](https://github.com/ollama/ollama/blob/main/docs/openai.md)

### Documentation
- [Ollama Setup Guide](docs/OLLAMA_SETUP.md) - Detailed Ollama configuration
- [Build & Test Guide](docs/BUILD_AND_TEST_GUIDE.md) - Complete setup and testing instructions

## Contributing

Contributions are welcome! Please see the main CUGA repository for contribution guidelines.

## License

This demo application follows the same license as the CUGA project.

## Support

For questions and support:
- GitHub Issues: [CUGA Issues](https://github.com/cuga-project/cuga-agent/issues)
- Discord: [Join Community](https://discord.gg/aH6rAEEW)
- Contact: [CUGA Team](https://forms.office.com/pages/responsepage.aspx?id=V3D2_MlQ1EqY8__KZK3Z6UtMUa14uFNMi1EyUFiZFGRUQklOQThLRjlYMFM2R1dYTk5GVTFMRzNZVi4u)