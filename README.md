# Simple AI Assistant

A lightweight Python AI assistant script using the OpenAI Python SDK configured to communicate with a local LLM runner (such as Ollama) via an OpenAI-compatible endpoint.

## Project Structure

```
Ai-assistant/
├── .gitignore               # Ignored files (venv, caches, etc.)
├── README.md                # Project documentation and setup guide
├── requirements.txt         # Project dependencies (openai)
└── simple-ai-assistant.py   # Main assistant script
```

## Prerequisites

1. **Python 3.8+** installed.
2. **Local LLM Runner** (e.g., [Ollama](https://ollama.com/)):
   - Install Ollama and pull the model:
     ```bash
     ollama pull qwen3:1.7b
     ```
   - Make sure Ollama is running at `http://127.0.0.1:11434`.

---

## Setup & Running on Any System

### 1. Clone the repository
```bash
git clone https://github.com/BhargavaGoli/Ai-assistant.git
cd Ai-assistant
```

### 2. Create and activate a virtual environment

- **macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

- **Windows (Command Prompt):**
  ```cmd
  python -m venv venv
  venv\Scripts\activate.bat
  ```

- **Windows (PowerShell):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the assistant
```bash
python simple-ai-assistant.py
```