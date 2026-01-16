# Football Scout Chatbot

AI-powered conversational interface for football player analysis using RAG (Retrieval-Augmented Generation) architecture with local LLM inference via Ollama.

## 🚀 Quick Start

### Prerequisites

1. **Python Environment**: Python 3.10+ with conda
2. **Ollama**: Local LLM runtime ([Download here](https://ollama.ai))
3. **Dependencies**: See `requirements.txt` in project root

### Setup Steps

#### 1. Install Ollama

Download and install Ollama from https://ollama.ai

Verify installation:
```bash
ollama --version
```

#### 2. Pull Required Models

```bash
# Chat generation model (3.8GB)
ollama pull phi3:mini

# Embedding model (274MB)
ollama pull nomic-embed-text:latest
```

Verify models are downloaded:
```bash
ollama list
```

Expected output:
```
NAME                        ID              SIZE     MODIFIED
phi3:mini                   ...             3.8 GB   ...
nomic-embed-text:latest     ...             274 MB   ...
```

#### 3. Start Ollama Server

**CRITICAL**: You must start the Ollama server BEFORE running the chatbot.

Open a **NEW terminal window** and run:
```bash
ollama serve
```

**Important**:
- Keep this terminal window **OPEN** while using the chatbot
- You should see: `Ollama is running on http://localhost:11434`
- DO NOT close this terminal or the chatbot will fail

Verify server is running (in a different terminal):
```bash
curl http://localhost:11434/api/tags
```

Expected: JSON response with available models

#### 4. Activate Python Environment

```bash
conda activate python_310_env
```

#### 5. Verify Setup (Optional but Recommended)

Before running the chatbot, test your Ollama setup:

```bash
python chatbot/test_ollama_connection.py
```

This script will verify:
- ✅ Ollama package is installed
- ✅ Server is running and accessible
- ✅ Required models are downloaded
- ✅ Chat and embedding generation work

If all tests pass, you're ready to run the chatbot!

#### 6. Run the Chatbot

```bash
streamlit run chatbot/chatbot_app.py
```

The chatbot should open in your browser at `http://localhost:8501`

## 🔍 Troubleshooting

### Error: "OLLAMA SERVER NOT RUNNING"

**Cause**: Ollama server not started

**Solution**:
1. Open a new terminal
2. Run `ollama serve`
3. Keep terminal open
4. Restart chatbot app

### Error: "Model not found: phi3:mini"

**Cause**: Required models not downloaded

**Solution**:
```bash
ollama pull phi3:mini
ollama pull nomic-embed-text:latest
```

### Error: Connection refused on localhost:11434

**Cause**: Firewall blocking port or Ollama not running

**Solution**:
1. Check firewall settings (allow port 11434)
2. Verify Ollama is running: `ollama serve`
3. Check port usage: `netstat -ano | findstr :11434` (Windows) or `lsof -i :11434` (Mac/Linux)

### Chatbot app starts but connection still fails

**Possible causes**:
1. Wrong Python environment (not python_310_env)
2. Ollama server crashed after starting
3. Port conflict

**Solutions**:
1. Verify environment: `conda activate python_310_env`
2. Restart Ollama server
3. Check Ollama server logs in the terminal running `ollama serve`

## 🏗️ Architecture

### RAG Pipeline

```
User Query
    ↓
Query Processor (intent classification, entity extraction)
    ↓
Context Builder (retrieve relevant players from ChromaDB)
    ↓
Response Generator (LLM generates natural language response)
    ↓
Chat Interface (display response with stats/charts)
```

### Components

- **`chatbot_app.py`**: Main Streamlit interface
- **`ollama/client.py`**: Ollama API wrapper for chat and embeddings
- **`vector_store/chroma_wrapper.py`**: ChromaDB wrapper for player embeddings
- **`retrieval/query_processor.py`**: Query analysis and intent classification
- **`retrieval/context_builder.py`**: Retrieves relevant context from vector DB
- **`response/generator.py`**: Natural language response generation
- **`utils/chat_memory.py`**: Conversation history management
- **`knowledge/`**: Domain knowledge base (tactical concepts, positions, etc.)

### Models Used

- **Chat Model**: `phi3:mini` (Microsoft Phi-3 Mini)
  - Size: 3.8GB
  - Context length: 128K tokens
  - Fast inference on CPU

- **Embedding Model**: `nomic-embed-text:latest`
  - Size: 274MB
  - Dimensions: 768
  - Max sequence: 8192 tokens

## 📊 Features

### Supported Queries

- **Player Search**: "Find CBs under 25 with Security > 80"
- **Player Comparison**: "Compare top scorers from BRI Liga 1"
- **Role Matching**: "Who fits ball-playing CB role best in Brazil Serie B?"
- **Statistics**: "Show stats for [player name]"
- **Similarity**: "Find players similar to [player name]"

### Data Modes

- **Test Mode**: 2 CSV files (~750 players) - Fast indexing for development
- **Production Mode**: All CSV files (10K+ players) - Full dataset

Toggle in sidebar under "Data Source"

## 🛠️ Development

### Running in Development Mode

Use Test Mode (default) for faster iteration:
1. Only indexes 2 CSV files (BRI Liga 1, Brazil Serie B)
2. ~750 players
3. Quick database rebuilds

### Rebuilding Database

If player data changes or you want to switch data modes:
1. Click "🔄 Rebuild Database" in sidebar
2. Wait for re-indexing to complete
3. Database persists across app restarts (stored in `.chroma/`)

### Adding New Knowledge

To add domain knowledge (tactical concepts, role definitions):
1. Add to `knowledge/` directory
2. Update `chroma_wrapper.index_knowledge()` method
3. Rebuild database

## 📝 Usage Examples

### Example 1: Find Young Defenders
```
Query: "Find the best young center backs in Brazil Serie B under age 23"

Response: [Lists top CBs with Security, Aerial Ability, Progressive Passing stats]
```

### Example 2: Role Matching
```
Query: "Who are the best ball-playing defenders in BRI Liga 1?"

Response: [Ranks players by Ball-Playing CB preset with key stats]
```

### Example 3: Player Comparison
```
Query: "Compare the top 3 scorers from BRI Liga 1"

Response: [Compares Clinical Finishing, Movement, Poaching attributes]
```

## ⚙️ Configuration

Edit `chatbot/ollama/config.py` to change:

- **Chat Model**: `DEFAULT_CHAT_MODEL = "phi3:mini"`
- **Embedding Model**: `DEFAULT_EMBED_MODEL = "nomic-embed-text:latest"`
- **Server Host**: `OLLAMA_DEFAULT_HOST = "http://localhost:11434"`
- **Timeout**: `OLLAMA_DEFAULT_TIMEOUT = 60`

### Using Different Models

To use a different chat model:
1. Pull the model: `ollama pull <model-name>`
2. Update `DEFAULT_CHAT_MODEL` in `config.py`
3. Restart chatbot app

Popular alternatives:
- `llama3.1:8b` - Larger, more capable (8B parameters)
- `mistral:latest` - Fast, good quality
- `gemma2:9b` - Google's model

## 🔒 Privacy & Security

- **100% Local**: All LLM inference runs on your machine
- **No API Keys**: No external API calls to OpenAI, Anthropic, etc.
- **No Data Sharing**: Player data stays on your local machine
- **Offline Capable**: Works without internet (after models are downloaded)

## 📚 Resources

- [Ollama Documentation](https://ollama.ai/docs)
- [Phi-3 Model Card](https://huggingface.co/microsoft/phi-3-mini-128k-instruct)
- [Nomic Embed Text](https://huggingface.co/nomic-ai/nomic-embed-text-v1)
- [ChromaDB Documentation](https://docs.trychroma.com)
- [Streamlit Documentation](https://docs.streamlit.io)

## 🐛 Known Issues

1. **First query slow**: Initial embedding generation takes ~5-10s (models loading into memory)
2. **Large datasets**: Indexing all CSVs takes ~2-3 minutes
3. **Memory usage**: With all players indexed, app uses ~2-3GB RAM

## 💡 Tips

- Use Test Mode during development for faster rebuilds
- Keep Ollama server terminal visible to monitor performance
- If responses are slow, check Ollama server terminal for errors
- Clear chat history regularly to maintain context relevance
- Rebuild database after adding new CSV files to `data/2025/`
