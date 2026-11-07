# AI Assistant

A Python AI assistant that talks to a local LLM (via [Ollama](https://ollama.com/)) through an OpenAI-compatible endpoint. It supports **tool calling** (function calling), so the model can fetch real data like the current time, the user's city, and live weather instead of guessing. It also demonstrates an **agent loop** that chains multiple tool calls, and **token streaming** for live, word-by-word responses.

## Features

- Chat with a local model through the OpenAI Python SDK (no cloud, no API costs).
- **Tool calling**: the model requests a tool, Python runs it, and the result is fed back for the final answer.
- **Agent loop**: chains dependent tools (e.g. find the user's city, then get that city's weather) up to a step limit.
- **Streaming**: responses print as they are generated.
- Config via a `.env` file (model, endpoint, debug logging).

## Project Structure

```
Ai-assistant/
├── .env                        # Config: MODEL, URL, API_KEY, DEBUG (not committed)
├── .gitignore                  # Ignored files (venv, .env, __pycache__)
├── README.md                   # This file
├── requirements.txt            # Dependencies: openai, python-dotenv, requests
├── simple-ai-assistant.py      # Original plain chat (no tools) — kept as a reference
├── assistant.py                # Chat assistant with the tool-calling agent loop
├── tools.py                    # Tool functions + their descriptions + run_tool()
├── try.py                      # Streaming + tool-calling version (agent loop)
├── stream-tokens-test.py       # Minimal token-streaming demo
├── stream-toolcalls-test.py    # Streaming + tool-calling test
└── Utilities/
    └── utilities.py            # log() helper (prints only when DEBUG=True)
```

## The tools

Defined in `tools.py`:

| Tool | What it does | Needs |
|------|--------------|-------|
| `get_current_time` | Returns the current date and time | nothing |
| `get_current_city` | Returns the user's home city | nothing |
| `get_city_weather` | Returns live weather for a city (via wttr.in) | `city` |

## Prerequisites

1. **Python 3.8+** installed.
2. **Ollama** installed and running at `http://127.0.0.1:11434`.
   - Pull a model that supports tool calling, for example:
     ```bash
     ollama pull qwen2.5:3b
     ```
   - `qwen2.5:3b` is recommended — it handles tool calling well on CPU-only machines. Tiny models (e.g. `qwen3:0.6b`) are unreliable for tools.

## Setup

### 1. Clone and enter the repo
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
- **Windows (PowerShell):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
- **Windows (Command Prompt):**
  ```cmd
  python -m venv venv
  venv\Scripts\activate.bat
  ```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file in the project root
```ini
MODEL=qwen2.5:3b
URL="http://127.0.0.1:11434/v1"
API_KEY="dummy"
DEBUG=True
```

- `MODEL` — the Ollama model to use. Must be pulled first.
- `URL` — the OpenAI-compatible endpoint Ollama exposes (note the `/v1`).
- `API_KEY` — any non-empty string; Ollama ignores it but the SDK requires one.
- `DEBUG` — set to `True` to print tool-call steps (which tool ran, its arguments, and its result). Set to `False` for a clean chat.

> `.env` is gitignored on purpose. Never commit it.

## Running

Full tool-calling assistant (agent loop):
```bash
python assistant.py
```

Streaming + tool-calling version:
```bash
python try.py
```

Plain chat (no tools), for reference:
```bash
python simple-ai-assistant.py
```

Type `exit` or `bye` to quit.

## Example session

```
you : what time is it?
tool called : get_current_time
LLM response : The current time is 2026-11-04 16:45:44.

you : what's the weather in my home?
tool called : get_current_city        -> Bangalore
tool called : get_city_weather        -> Bangalore: ☁️ +27°C
LLM response : The weather in your home, Bangalore, is cloudy, +27°C.
```

## How tool calling works

1. Your message is sent to the model along with the list of available tools.
2. If the model needs real data, it responds with a **tool call** (a tool name + arguments) instead of text.
3. The code runs the matching Python function via `run_tool()` and appends the result as a `tool` message.
4. The model is called again; it reads the result and produces the final answer.
5. For chained tasks (city → weather), the loop repeats one tool at a time, feeding each result into the next call, up to `MAX_STEPS`.

## Notes

- This project runs entirely locally; performance depends on your CPU/GPU. On CPU-only machines, keep to small models (0.6B–4B).
- Tool-calling reliability depends heavily on the model. `qwen2.5:3b` is a good balance of speed and tool-use accuracy for local use.
