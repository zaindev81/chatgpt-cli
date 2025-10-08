# Import required libraries
from openai import OpenAI
import os
import argparse
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Define default model and context file (in the same directory as main.py)
DEFAULT_MODEL = "gpt-4.1-mini"
SCRIPT_DIR = Path(__file__).parent
CONTEXT_FILE = SCRIPT_DIR / ".chatgpt_context.json"


def strip_markdown(text: str) -> str:
    """Remove basic markdown symbols from text"""
    return (
        text.replace("**", "")  # Remove bold markers
            .replace("*", "")    # Remove italic markers
            .replace("`", "")    # Remove code markers
    )


def load_context() -> dict:
    """Load context settings from file, return defaults if file doesn't exist"""
    if CONTEXT_FILE.exists():
        with open(CONTEXT_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    # Return default context structure
    return {
        "system_prompt": "",        # System prompt for continuous instructions
        "conversation_history": [], # Chat history
        "modes": {                  # Various mode settings
            "translate_to": "",
            "improve_language": False,
            "continuous_mode": ""
        }
    }


def save_context(context: dict):
    """Save context settings to file"""
    with open(CONTEXT_FILE, 'w', encoding='utf-8') as f:
        json.dump(context, f, ensure_ascii=False, indent=2)


def chat_with_gpt(client: OpenAI, prompt: str, model: str, strip_md: bool, context: dict) -> str:
    """Chat with GPT considering context and conversation history"""
    messages = []

    # Add system prompt if there are continuous instructions
    if context["system_prompt"]:
        messages.append({"role": "system", "content": context["system_prompt"]})

    # Add conversation history (last 20 messages to save memory)
    messages.extend(context["conversation_history"][-20:])

    # Add current user message
    messages.append({"role": "user", "content": prompt})

    # Call OpenAI API
    resp = client.chat.completions.create(
        model=model,
        messages=messages,
    )
    result = (resp.choices[0].message.content or "").strip()

    # Update conversation history with user message and assistant response
    context["conversation_history"].append({"role": "user", "content": prompt})
    context["conversation_history"].append({"role": "assistant", "content": result})

    # Return result with markdown stripped if option is enabled
    return strip_markdown(result) if strip_md else result


def main():
    """Main function: parse command line arguments and start chat"""
    # Set up command line argument parser
    parser = argparse.ArgumentParser(description="Chat with OpenAI GPT models.")
    parser.add_argument(
        "--model",
        type=str,
        default=DEFAULT_MODEL,
        help=f"Model name to use (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--strip-markdown",
        action="store_true",
        help="Strip basic markdown symbols from response",
    )
    parser.add_argument(
        "--set-system",
        type=str,
        help="Set system prompt (e.g., 'Translate to English', 'Improve my English')",
    )
    parser.add_argument(
        "--clear-context",
        action="store_true",
        help="Clear conversation history and system prompt",
    )
    args = parser.parse_args()

    # Load saved context
    context = load_context()

    # Handle context clear option
    if args.clear_context:
        context = {
            "system_prompt": "",
            "conversation_history": [],
            "modes": {"translate_to": "", "improve_language": False, "continuous_mode": ""}
        }
        save_context(context)
        print("Context cleared!")
        return

    # Handle system prompt setting option
    if args.set_system:
        context["system_prompt"] = args.set_system
        save_context(context)
        print(f"System prompt set: {args.set_system}")
        return

    # Check OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Please set the OPENAI_API_KEY environment variable.")

    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)

    # Display current settings
    print(f"Using model: {args.model}")
    if context["system_prompt"]:
        print(f"System prompt: {context['system_prompt']}")
    print("Special commands:")
    print("  /clear - Clear conversation history")
    print("  /system <prompt> - Set system prompt")
    print("  /translate <language> - Set translation mode")
    print("  /improve - Enable English improvement mode")
    print("Press Ctrl+C to exit.\n")

    # Main chat loop
    try:
        while True:
            user_input = input("You: ")
            if not user_input.strip():
                continue

            # Handle special commands
            if user_input.startswith("/"):
                if user_input == "/clear":
                    context["conversation_history"] = []
                    save_context(context)
                    print("Conversation history cleared!")
                    continue
                elif user_input.startswith("/system "):
                    context["system_prompt"] = user_input[8:]
                    save_context(context)
                    print(f"System prompt set: {context['system_prompt']}")
                    continue
                elif user_input.startswith("/translate "):
                    lang = user_input[11:]
                    context["system_prompt"] = f"Translate the following text to {lang}:"
                    save_context(context)
                    print(f"Translation mode set to: {lang}")
                    continue
                elif user_input == "/improve":
                    context["system_prompt"] = "Please improve my English and explain the corrections:"
                    save_context(context)
                    print("English improvement mode activated!")
                    continue

            # Chat with GPT and display result
            reply = chat_with_gpt(client, user_input, args.model, args.strip_markdown, context)
            print("GPT:", reply)

            # Save context to file
            save_context(context)

    except (KeyboardInterrupt, EOFError):
        print("\nBye!")


if __name__ == "__main__":
    main()
