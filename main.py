from openai import OpenAI
import os
import argparse
from dotenv import load_dotenv

load_dotenv()

DEFAULT_MODEL = "gpt-4.1-mini"
# DEFAULT_MODEL = "gpt-4o-mini"

def strip_markdown(text: str) -> str:
    return (
        text.replace("**", "")
            .replace("*", "")
            .replace("`", "")
    )


def chat_with_gpt(client: OpenAI, prompt: str, model: str, strip_md: bool) -> str:
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    result = (resp.choices[0].message.content or "").strip()
    return strip_markdown(result) if strip_md else result


def main():
    parser = argparse.ArgumentParser(description="Chat with OpenAI GPT models.")
    parser.add_argument(
        "--model",
        type=str,
        default=DEFAULT_MODEL,
        help=f"Model name (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--strip-markdown",
        action="store_true",
        help="Strip basic markdown from the response.",
    )
    args = parser.parse_args()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Please set the OPENAI_API_KEY environment variable.")

    client = OpenAI(api_key=api_key)

    print(f"Using model: {args.model}")
    print("Press Ctrl+C to exit.\n")

    try:
        while True:
            user_input = input("You: ")
            if not user_input.strip():
                continue
            reply = chat_with_gpt(client, user_input, args.model, args.strip_markdown)
            print("GPT:", reply)
    except (KeyboardInterrupt, EOFError):
        print("\nBye!")


if __name__ == "__main__":
    main()
