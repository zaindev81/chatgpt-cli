# chatpgt-cli

A simple CLI tool for chatting with OpenAI's GPT models.

## Installation

```bash
source .venv/bin/activate
uv sync
```

## Configuration

### **Option 1: Using `.env` file (recommended)**

1. Create a `.env` file by copying the example:

   ```bash
   cp .env.example .env
   ```
2. Open `.env` and add your API key:

   ```env
   OPENAI_API_KEY=your_api_key_here
   ```

> ⚠ **Important:**
>
> * Never commit `.env` to GitHub.
> * Add `.env` to your `.gitignore` to keep your API key safe.

---

### **Option 2: Using environment variables directly**

```bash
export OPENAI_API_KEY=your_api_key_here
```

## Usage

### Basic Usage

Run directly:

```bash
python main.py [--model MODEL] [--strip-markdown]
```

Or if installed as a package:

```bash
chatpgt-cli [--model MODEL] [--strip-markdown]
```

**Command Line Options:**
- `--model`: Model name (default: gpt-4.1-mini)
- `--strip-markdown`: Strip basic markdown (asterisks, backticks) from the response
- `--set-system`: Set system prompt for continuous instructions
- `--clear-context`: Clear conversation history and system prompt

### Context & Memory Features

This CLI now supports **persistent context and memory** across sessions:

#### System Prompts (Continuous Instructions)
Set persistent instructions that apply to all future messages:

```bash
# Set translation mode
python main.py --set-system "Translate everything to Japanese"

# Set English improvement mode
python main.py --set-system "Please improve my English and explain corrections"

# Clear all context
python main.py --clear-context
```

#### In-Chat Commands
During a chat session, use these special commands:

- `/clear` - Clear conversation history
- `/system <prompt>` - Set system prompt
- `/translate <language>` - Set translation mode
- `/improve` - Enable English improvement mode

#### Examples

**Translation Mode:**
```bash
python main.py --set-system "Translate to Chinese"
python main.py
You: Hello, How are you
GPT: 你好，你好吗？
```

**English Improvement Mode:**
```bash
python main.py --set-system "Improve my English and explain corrections"
python main.py
You: I am very good in English
GPT: I am very good at English. (Correction: Use "good at" when talking about skills)
```

**In-Chat Mode Switching:**
```
You: /translate Spanish
Translation mode set to: Spanish
You: Good morning
GPT: Buenos días
You: /improve
English improvement mode activated!
You: I have much books
GPT: I have many books. (Correction: Use "many" with countable nouns like "books")
```

#### Context Storage
- Conversation history and settings are automatically saved to `.chatgpt_context.json`
- Context persists between sessions
- Last 20 messages are kept in memory for context

---

## License

MIT License