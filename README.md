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

Run directly:

```bash
python main.py [--model MODEL] [--strip-markdown]
```

Or if installed as a package:

```bash
chatpgt-cli [--model MODEL] [--strip-markdown]
```

- `--model`: Model name (default: gpt-4.1-mini)
- `--strip-markdown`: Strip basic markdown (asterisks, backticks) from the response.

---

## License

MIT License