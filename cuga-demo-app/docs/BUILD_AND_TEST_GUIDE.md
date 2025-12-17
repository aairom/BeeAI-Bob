# CUGA Demo Application - Build Process, Purpose & Testing Guide

## Table of Contents
1. [Application Purpose](#application-purpose)
2. [Build Process](#build-process)
3. [Architecture Overview](#architecture-overview)
4. [How to Run](#how-to-run)
5. [Testing Guide](#testing-guide)
6. [Sample Test Inputs](#sample-test-inputs)

---

## Application Purpose

### What is CUGA?
CUGA (Collaborative Universal Generative Agent) is a state-of-the-art AI agent framework that achieves:
- 🥇 #1 ranking on AppWorld benchmark (750 real-world tasks across 457 APIs)
- 🥈 Top-tier performance on WebArena (complex autonomous web agent benchmark)

### Purpose of This Demo Application
This demonstration application showcases how to:

1. **Integrate CUGA** with various LLM providers (Ollama, OpenAI, watsonx, Azure, OpenRouter)
2. **Execute Complex Tasks** through natural language instructions
3. **Implement Custom Tools** via OpenAPI specs, MCP servers, and LangChain
4. **Switch Between Reasoning Modes** (fast, balanced, accurate) based on task requirements
5. **Handle Multi-Step Workflows** with automatic task decomposition
6. **Demonstrate API, Web, and Hybrid Modes** for different use cases
7. **Run Locally with Ollama** for free, private, and offline AI capabilities

### Key Use Cases Demonstrated

- **CRM Operations**: Query accounts, contacts, and sales data
- **Data Analysis**: Process and analyze business metrics
- **Web Automation**: Browser-based interactions and data extraction
- **Hybrid Workflows**: Combine API calls with web interactions
- **Custom Tool Integration**: Extend agent capabilities with domain-specific tools

---

## Build Process

### Step 1: Project Structure Creation

The application was built with a modular architecture:

```
cuga-demo-app/
├── config/              # Configuration files
│   ├── settings.toml    # Main CUGA settings
│   ├── modes/           # Reasoning mode configs
│   └── tools/           # Tool registry
├── src/                 # Source code
│   ├── main.py          # CLI entry point
│   ├── agents/          # Specialized agents
│   ├── tools/           # Custom tools
│   └── examples/        # Usage examples
├── docs/                # Documentation
└── tests/               # Test suite
```

### Step 2: Core Components Implementation

#### 2.1 Main Application (`src/main.py`)
- **CLI Interface**: Built with Click for command-line interactions
- **Configuration Management**: TOML-based settings with environment variable support
- **Interactive Mode**: Real-time task execution with user feedback
- **Setup Verification**: Automated environment checks

#### 2.2 API Agent (`src/agents/api_agent.py`)
- **Purpose**: Handle API-focused tasks
- **Features**:
  - REST API interactions
  - Multi-step API workflows
  - Result aggregation
  - Execution history tracking

#### 2.3 Custom Tools (`src/tools/custom_tools.py`)
- **Calculator Tool**: Safe mathematical expression evaluation
- **Sentiment Analyzer**: Text sentiment classification
- **Data Processor**: JSON data transformation (filter, sort, aggregate)

#### 2.4 OpenAPI Integration (`src/tools/openapi_specs/crm_api.yaml`)
- **CRM API Specification**: Complete OpenAPI 3.0 spec
- **Endpoints**: Accounts, contacts, and relationships
- **Authentication**: Bearer token support

### Step 3: Configuration System

#### 3.1 Environment Variables (`.env.example`)
- LLM provider credentials
- Model selection
- Feature flags
- Optional service configurations

#### 3.2 TOML Configuration (`config/settings.toml`)
- Reasoning modes (fast/balanced/accurate)
- Task execution modes (api/web/hybrid)
- Agent behavior settings
- Tool registry configuration
- Memory and caching options

#### 3.3 Mode-Specific Configs (`config/modes/`)
- **Fast Mode**: Optimized for speed
- **Balanced Mode**: Default, good trade-off
- **Accurate Mode**: Maximum precision

### Step 4: Example Implementations

#### 4.1 Basic Usage (`src/examples/basic_usage.py`)
Demonstrates:
- Simple task execution
- Parameterized queries
- Error handling
- Multi-step workflows
- Mode comparison

---

## Architecture Overview

### Component Interaction Flow

```
User Input (Natural Language)
    ↓
CLI Interface (main.py)
    ↓
Configuration Loader (settings.toml + .env)
    ↓
Agent Selection (API/Web/Hybrid)
    ↓
Task Planner (CUGA Core)
    ↓
Tool Registry (OpenAPI/MCP/LangChain)
    ↓
Executor (API calls, code execution, web actions)
    ↓
Result Aggregator
    ↓
Formatted Output
```

### Key Design Patterns

1. **Strategy Pattern**: Different reasoning modes (fast/balanced/accurate)
2. **Factory Pattern**: Agent creation based on task mode
3. **Observer Pattern**: Execution history tracking
4. **Adapter Pattern**: Tool integration (OpenAPI, MCP, LangChain)

---

## How to Run

### Prerequisites Installation

```bash
# 1. Navigate to project directory
cd cuga-demo-app

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your LLM provider settings
```

### Configuration Setup

#### Option A: Using Ollama (Recommended for Getting Started)

**Step 1: Install Ollama**
```bash
# Visit https://ollama.ai and download for your OS
# Or use package managers:
# macOS: brew install ollama
# Linux: curl -fsSL https://ollama.com/install.sh | sh
```

**Step 2: Start Ollama and Pull a Model**
```bash
# Start Ollama service
ollama serve

# In another terminal, pull a model
ollama pull llama3.2

# Verify it's running
curl http://localhost:11434/api/tags
```

**Step 3: Configure .env for Ollama**
```env
# Ollama Configuration (Local, Free, Private)
OPENAI_API_KEY=ollama
OPENAI_BASE_URL=http://localhost:11434/v1
AGENT_SETTING_CONFIG="settings.openai.toml"
MODEL_NAME=llama3.2

# Application Settings
APP_MODE=development
LOG_LEVEL=INFO
```

#### Option B: Using OpenAI or Other Cloud Providers

Edit `.env` file:
```env
# OpenAI Configuration
OPENAI_API_KEY=sk-your-key-here
AGENT_SETTING_CONFIG="settings.openai.toml"
MODEL_NAME=gpt-4o
```

For other providers (watsonx, Azure, OpenRouter), see `.env.example` for configuration options.

Edit `config/settings.toml` for features:
```toml
[features]
cuga_mode = "balanced"  # fast, balanced, or accurate

[advanced_features]
mode = "api"  # api, web, or hybrid
```

### Running the Application

#### 1. Verify Setup
```bash
python src/main.py check-setup
```

**Expected output with Ollama:**
```
╭─────────────────────────────────────╮
│     CUGA Setup Check                │
╰─────────────────────────────────────╯

Setup Status
┏━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┓
┃ Component      ┃ Status         ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━┩
│ LLM Provider   │ Ollama (Local) │
│ Ollama Service │ ✓ Running      │
│ Config File    │ ✓              │
│ .env File      │ ✓              │
└────────────────┴────────────────┘

✓ Ollama is configured and running!
Model: llama3.2
```

**Expected output with cloud providers:**
```
╭─────────────────────────────────────╮
│     CUGA Setup Check                │
╰─────────────────────────────────────╯

Setup Status
┏━━━━━━━━━━━━━┳━━━━━━━━┓
┃ Component   ┃ Status ┃
┡━━━━━━━━━━━━━╇━━━━━━━━┩
│ API Key     │ ✓      │
│ Config File │ ✓      │
│ .env File   │ ✓      │
└─────────────┴────────┘
```

#### 2. View Examples
```bash
python src/main.py examples
```

#### 3. Run Single Task
```bash
python src/main.py run --task "get top 5 accounts by revenue"
```

#### 4. Interactive Mode
```bash
python src/main.py interactive
```

Interactive commands:
- Type any task to execute
- `config` - View current configuration
- `help` - Show available commands
- `exit` or `quit` - End session

#### 5. Run Example Scripts

**Basic Usage Examples:**
```bash
python src/examples/basic_usage.py
```

**API Agent Demo:**
```bash
python src/agents/api_agent.py
```

**Custom Tools Demo:**
```bash
python src/tools/custom_tools.py
```

---

## Testing Guide

### Manual Testing

#### Test 1: Setup Verification
```bash
python src/main.py check-setup
```
**Expected**: All components show ✓ status

#### Test 2: Basic Task Execution
```bash
python src/examples/basic_usage.py
```
**Expected**: 5 examples execute successfully with detailed output

#### Test 3: API Agent
```bash
python src/agents/api_agent.py
```
**Expected**: 
- Account query returns 2 accounts
- Sales query shows revenue breakdown
- Execution history displays 2 tasks

#### Test 4: Custom Tools
```bash
python src/tools/custom_tools.py
```
**Expected**:
- Calculator: (10 + 5) * 2 = 30
- Sentiment: Positive sentiment detected
- Data Processor: Filtering and aggregation work

#### Test 5: Interactive Mode
```bash
python src/main.py interactive
```
Test commands:
```
CUGA> config
CUGA> get top 3 accounts by revenue
CUGA> help
CUGA> exit
```

### Automated Testing

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_agents.py

# Verbose output
pytest -v tests/
```

---

## Sample Test Inputs

### Category 1: CRM Operations

#### Test Input 1.1: Simple Account Query
```
Task: "List all accounts in the CRM system"

Expected Output:
- Status: success
- Data: Array of accounts with id, name, revenue
- Execution time: ~2-3 seconds
```

#### Test Input 1.2: Filtered Account Query
```
Task: "Get top 5 accounts by revenue from digital sales"

Expected Output:
- Status: success
- Data: 5 accounts sorted by revenue (descending)
- Parameters: limit=5, sort=revenue, order=desc
- Execution time: ~1-2 seconds
```

#### Test Input 1.3: Account with Contacts
```
Task: "Find the highest revenue account and get its contact details"

Expected Output:
- Status: success
- Steps: 3 (get accounts, select top, fetch contacts)
- Data: Account info + array of contacts
- Execution time: ~2-3 seconds
```

### Category 2: Data Analysis

#### Test Input 2.1: Revenue Analysis
```
Task: "Show Q4 2024 revenue breakdown"

Expected Output:
- Status: success
- Data: total_revenue, growth_rate, top_products
- API calls: 1 (GET /sales/revenue)
- Execution time: ~2 seconds
```

#### Test Input 2.2: Mathematical Calculation
```
Task: "Calculate (150 + 75) * 3 - 50"

Expected Output:
- Result: 625
- Tool used: calculator
- Execution time: <1 second
```

#### Test Input 2.3: Sentiment Analysis
```
Task: "Analyze sentiment: This product is excellent and I love it!"

Expected Output:
- Sentiment: positive
- Confidence: 0.70-0.90
- Tool used: sentiment_analyzer
- Execution time: <1 second
```

### Category 3: Data Processing

#### Test Input 3.1: Filter Operation
```
Task: "Filter accounts with revenue greater than 1 million"

Input Data:
[
  {"name": "Acme Corp", "revenue": 1000000},
  {"name": "TechStart", "revenue": 750000},
  {"name": "Global Solutions", "revenue": 2000000}
]

Expected Output:
[
  {"name": "Acme Corp", "revenue": 1000000},
  {"name": "Global Solutions", "revenue": 2000000}
]
```

#### Test Input 3.2: Sort Operation
```
Task: "Sort accounts by revenue in descending order"

Expected Output:
- Accounts sorted: revenue DESC
- Tool used: data_processor
- Operation: sort
```

#### Test Input 3.3: Aggregate Operation
```
Task: "Calculate total revenue across all accounts"

Expected Output:
- Total: sum of all revenues
- Count: number of accounts
- Tool used: data_processor
- Operation: aggregate
```

### Category 4: Multi-Step Workflows

#### Test Input 4.1: Complex Query
```
Task: "Get the top 3 accounts by revenue, then find contacts for each"

Expected Steps:
1. Query accounts with sort and limit
2. For each account, fetch contacts
3. Aggregate results

Expected Output:
- 3 accounts with their contacts
- Total execution time: ~3-5 seconds
```

#### Test Input 4.2: Conditional Logic
```
Task: "If total revenue exceeds 5 million, get top performers, otherwise get all accounts"

Expected Behavior:
- Evaluate condition
- Execute appropriate branch
- Return relevant data
```

### Category 5: Error Handling

#### Test Input 5.1: Invalid Input
```
Task: "Get account with ID: -999"

Expected Output:
- Status: error
- Error type: ValidationError
- Message: "Invalid account ID: -999"
- Details: "Account ID must be a positive integer"
```

#### Test Input 5.2: Invalid Expression
```
Task: "Calculate: 10 + abc"

Expected Output:
- Status: error
- Message: "Invalid characters in expression"
- Tool: calculator
```

### Category 6: Mode Comparison

#### Test Input 6.1: Same Task, Different Modes
```
Task: "Analyze sales trends for Q4 2024"

Fast Mode:
- Execution time: ~1.2s
- Steps: 3
- Accuracy: good

Balanced Mode:
- Execution time: ~2.5s
- Steps: 5
- Accuracy: very good

Accurate Mode:
- Execution time: ~4.8s
- Steps: 8
- Accuracy: excellent
```

---

## Performance Benchmarks

### Expected Performance Metrics

| Task Type | Fast Mode | Balanced Mode | Accurate Mode |
|-----------|-----------|---------------|---------------|
| Simple Query | 0.5-1s | 1-2s | 2-3s |
| Multi-step | 1-2s | 2-3s | 4-6s |
| Complex Analysis | 2-3s | 3-5s | 6-10s |

### Resource Usage

- **Memory**: ~100-200 MB (base)
- **CPU**: Low (mostly I/O bound)
- **Network**: Depends on API calls

---

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: Ollama Not Running
```bash
# Problem: "Ollama Service: ✗ Not accessible"
# Solution: Start Ollama service
ollama serve

# Or check if it's already running
curl http://localhost:11434/api/tags

# On macOS/Linux with systemd
systemctl start ollama
```

#### Issue 2: Ollama Model Not Found
```bash
# Problem: "model 'llama3.2' not found"
# Solution: Pull the model first
ollama pull llama3.2

# List available models
ollama list

# Try a different model
MODEL_NAME=phi3 python src/main.py check-setup
```

#### Issue 3: Import Errors
```bash
# Solution: Ensure virtual environment is activated
source .venv/bin/activate
pip install -r requirements.txt
```

#### Issue 4: API Key Not Found (Cloud Providers)
```bash
# Solution: Check .env file exists and contains valid keys
cat .env | grep API_KEY
```

#### Issue 5: Configuration Not Loaded
```bash
# Solution: Verify config file paths
ls -la config/settings.toml
ls -la config/modes/
```

#### Issue 6: Slow Performance with Ollama
```bash
# Solution 1: Use a smaller/faster model
MODEL_NAME=phi3 python src/main.py interactive

# Solution 2: Use quantized models
ollama pull llama3.2:8b-q4_0

# Solution 3: Check GPU usage
ollama ps

# Solution 4: Reduce context in mode configs
# Edit config/modes/fast.toml and reduce max_tokens
```

#### Issue 7: Tool Not Found
```bash
# Solution: Check tool registry
cat config/tools/mcp_servers.yaml
```

---

## Next Steps

After testing the demo application:

1. **Start with Ollama (Recommended)**
   - Install Ollama from https://ollama.ai
   - Pull a model: `ollama pull llama3.2`
   - Configure .env for Ollama (see above)
   - Run: `python src/main.py check-setup`
   - No API costs, complete privacy!

2. **Explore Advanced Features**
   - Enable memory for learning
   - Try web/hybrid modes
   - Set up custom MCP servers
   - Experiment with different models

3. **Integrate with Your Systems**
   - Add your OpenAPI specifications
   - Create custom tools for your domain
   - Configure authentication

4. **Production Deployment**
   - Set up proper logging
   - Configure monitoring
   - Implement rate limiting
   - Add security measures
   - Consider cloud providers for scale

5. **Join the Community**
   - GitHub: [CUGA Repository](https://github.com/cuga-project/cuga-agent)
   - Discord: [Community Chat](https://discord.gg/aH6rAEEW)
   - Try Live: [HuggingFace Space](https://huggingface.co/spaces/ibm-research/cuga-agent)
   - Ollama: [Documentation](https://github.com/ollama/ollama)

---

## Conclusion

This demo application provides a comprehensive foundation for understanding and implementing CUGA agents. The modular architecture allows easy extension and customization for specific use cases.

**Key Takeaways:**
- ✅ CUGA simplifies complex task automation
- ✅ Works with Ollama for free, local, and private AI
- ✅ Multiple reasoning modes optimize for different scenarios
- ✅ Extensible tool system supports custom integrations
- ✅ Production-ready architecture with proper error handling
- ✅ Comprehensive testing ensures reliability
- ✅ Easy to switch between local (Ollama) and cloud providers

**Quick Start with Ollama:**
```bash
# 1. Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 2. Pull a model
ollama pull llama3.2

# 3. Configure
cp .env.example .env
# Set: OPENAI_API_KEY=ollama, OPENAI_BASE_URL=http://localhost:11434/v1

# 4. Run
python src/main.py check-setup
python src/main.py interactive
```

For questions or support, refer to the official CUGA documentation or join the community channels.

---

**Document Version**: 1.1
**Last Updated**: December 17, 2024
**Author**: Bob (AI Software Engineer)
**Changes**: Added comprehensive Ollama support and configuration