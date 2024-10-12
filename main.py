import os
import time
from typing import List, Dict

from cerebras.cloud.sdk import Cerebras

MODEL_ID = "llama3.1-8b"
SYSTEM_MESSAGE = {"role": "system", "content": "You are a helpful assistant."}


def setup_cerebras_client() -> Cerebras:
    """Set up and return the Cerebras client."""
    api_key = os.getenv("CEREBRAS_API_KEY")
    if not api_key:
        raise ValueError("Missing Cerebras API Key.")
    return Cerebras(api_key=api_key)


def generate_response(
    client: Cerebras,
    prompt: str,
    chat_history: List[Dict[str, str]]
) -> Dict[str, str]:
    """Generate a response using the Cerebras client."""
    chat_history.append({"role": "user", "content": prompt})
    response = client.chat.completions.create(
        messages=chat_history,
        model=MODEL_ID,
    )
    return response


def print_response(response: Dict[str, str]) -> None:
    """Print the response and performance metrics."""
    message = response.choices[0].message.content

    for char in message:
        print(char, end="", flush=True)
        time.sleep(0.02)
    print()

    total_tokens = response.usage.total_tokens
    total_time = response.time_info.total_time
    tokens_per_second = total_tokens / total_time
    print(f"(Tokens per second: {tokens_per_second:.2f})")
    print()


def main():
    """Main function to run the chat application."""
    client = setup_cerebras_client()
    chat_history = [SYSTEM_MESSAGE]

    welcoming_text = f"""
    Welcome to {MODEL_ID} Text Generator made by (Awan)
    Happy chat and talk with your {MODEL_ID} AI Generative Model
    Addhe Warman Putra - (Awan)
    Type 'exit()' to exit from program
    """
    print(welcoming_text)

    while True:
        user_input = input("> ")
        if user_input.lower() == "exit()":
            break

        response = generate_response(client, user_input, chat_history)
        chat_history.append({
            "role": "assistant",
            "content": response.choices[0].message.content
        })
        print_response(response)


if __name__ == "__main__":
    main()
