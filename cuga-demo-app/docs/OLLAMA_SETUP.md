# Using CUGA Demo App with Local Ollama

This guide explains how to configure the CUGA demo application to work with a local Ollama instance.

## Prerequisites

1. **Install Ollama**: Download and install from [ollama.ai](https://ollama.ai)
2. **Pull a model**: Run `ollama pull llama3.2` (or any other model)
3. **Verify Ollama is running**: Check `http://localhost:11434` is accessible

## Configuration Steps

### 1. Create/Update Your `.env` File

Copy `.env.example` to `.env` and configure it for Ollama:

```bash
cp .env.example .env
```

### 2. Configure Environment Variables

Add the following to your `.env` file:

```env
# Ollama Configuration (OpenAI-compatible API)
OPENAI_API_KEY=ollama
OPENAI_BASE_URL=http://localhost:11434/v1
AGENT_SETTING_CONFIG="settings.openai.toml"
MODEL_NAME=llama3.2

# Application Settings
APP_MODE=development
LOG_LEVEL=INFO
```

### 3. Supported Ollama Models

You can use any model available in Ollama. Popular choices:

- **llama3.2** - Latest Llama model (recommended)
- **llama3.1** - Previous Llama version
- **mistral** - Mistral AI model
- **codellama** - Specialized for code tasks
- **phi3** - Microsoft's efficient model
- **qwen2.5** - Alibaba's model

To change models, update the `MODEL_NAME` in your `.env` file:

```env
MODEL_NAME=mistral
```

### 4. Verify Ollama is Running

Before running the application, ensure Ollama is active:

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Or test the OpenAI-compatible endpoint
curl http://localhost:11434/v1/models
```

### 5. Run the Application

```bash
# Check setup
python src/main.py check-setup

# Run a task
python src/main.py run --task "analyze this data"

# Interactive mode
python src/main.py interactive
```

## Performance Considerations

### Model Selection
- **Fast mode**: Use smaller models like `phi3` or `llama3.2:8b`
- **Balanced mode**: Use `llama3.2` or `mistral`
- **Accurate mode**: Use larger models like `llama3.1:70b` (requires significant RAM)

### Hardware Requirements
- **Minimum**: 8GB RAM for 7B-8B parameter models
- **Recommended**: 16GB RAM for 13B parameter models
- **High-end**: 32GB+ RAM for 70B parameter models

### Optimization Tips

1. **Use quantized models** for better performance:
   ```bash
   ollama pull llama3.2:8b-q4_0
   ```

2. **Adjust context window** in mode configs:
   ```toml
   # config/modes/fast.toml
   [model]
   max_tokens = 2048  # Reduce for faster responses
   ```

3. **Enable GPU acceleration** (if available):
   - Ollama automatically uses GPU when available
   - Check with: `ollama ps`

## Troubleshooting

### Connection Issues

**Problem**: Cannot connect to Ollama
```
Error: Connection refused at http://localhost:11434
```

**Solution**:
```bash
# Start Ollama service
ollama serve

# Or on macOS/Linux
systemctl start ollama
```

### Model Not Found

**Problem**: Model not available
```
Error: model 'llama3.2' not found
```

**Solution**:
```bash
# Pull the model first
ollama pull llama3.2

# List available models
ollama list
```

### Slow Performance

**Problem**: Responses are very slow

**Solutions**:
1. Use a smaller model: `MODEL_NAME=phi3`
2. Reduce max_tokens in config files
3. Use quantized versions: `llama3.2:8b-q4_0`
4. Ensure GPU is being used: `ollama ps`

### Memory Issues

**Problem**: Out of memory errors

**Solutions**:
1. Use smaller models (7B-8B parameters)
2. Close other applications
3. Use quantized models (q4_0, q4_1)
4. Reduce context window size

## Advanced Configuration

### Custom Ollama Port

If Ollama runs on a different port:

```env
OPENAI_BASE_URL=http://localhost:8080/v1
```

### Remote Ollama Instance

To use Ollama on another machine:

```env
OPENAI_BASE_URL=http://192.168.1.100:11434/v1
```

### Multiple Models

Switch between models dynamically:

```bash
# Use different models for different tasks
MODEL_NAME=codellama python src/main.py run --task "write a function"
MODEL_NAME=llama3.2 python src/main.py run --task "analyze data"
```

## Comparison with Cloud Providers

| Feature | Ollama (Local) | OpenAI (Cloud) |
|---------|---------------|----------------|
| Cost | Free | Pay per token |
| Privacy | Complete | Data sent to cloud |
| Speed | Depends on hardware | Generally faster |
| Models | Open source | Proprietary |
| Setup | Requires installation | API key only |
| Offline | Works offline | Requires internet |

## Example Usage

```bash
# 1. Start Ollama
ollama serve

# 2. Pull a model
ollama pull llama3.2

# 3. Configure .env for Ollama
cat > .env << EOF
OPENAI_API_KEY=ollama
OPENAI_BASE_URL=http://localhost:11434/v1
AGENT_SETTING_CONFIG="settings.openai.toml"
MODEL_NAME=llama3.2
APP_MODE=development
LOG_LEVEL=INFO
EOF

# 4. Run the application
python src/main.py check-setup
python src/main.py interactive
```

## Benefits of Using Ollama

1. **Privacy**: All data stays on your machine
2. **Cost**: No API fees
3. **Offline**: Works without internet
4. **Customization**: Full control over models
5. **Experimentation**: Try different models easily

## Limitations

1. **Performance**: Slower than cloud APIs (depends on hardware)
2. **Model Size**: Limited by available RAM
3. **Features**: Some advanced features may not be available
4. **Maintenance**: Need to manage models and updates

## Resources

- [Ollama Documentation](https://github.com/ollama/ollama)
- [Ollama Model Library](https://ollama.ai/library)
- [OpenAI API Compatibility](https://github.com/ollama/ollama/blob/main/docs/openai.md)

---

**Note**: This application is designed to work with any OpenAI-compatible API, making it easy to switch between Ollama, OpenAI, and other providers by simply changing environment variables.