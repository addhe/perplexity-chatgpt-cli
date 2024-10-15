import time
import os
import sys
from typing import List, Dict, Optional, Any
from cerebras.cloud.sdk import Cerebras

cerebras_client = None  # Initialize it to None

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Import configuration
from config import MODEL_ID, SYSTEM_MESSAGE, API_KEY, CHAR_DELAY

# Move Cerebras to the module level
cerebras_client = Cerebras(api_key=API_KEY)

def setup_cerebras_client() -> Cerebras:
    if not API_KEY:
        raise ValueError("Missing Cerebras API Key.")
    return cerebras_client

def generate_response(
    client: Cerebras,
    prompt: str,
    chat_history: List[Dict[str, str]]
) -> Optional[Any]:
    chat_history.append({"role": "user", "content": prompt})
    try:
        return client.chat.completions.create(
            messages=chat_history,
            model=MODEL_ID,
        )
    except Exception as e:
        print(f"Error generating response: {e}")
        return None

def print_response(response: Optional[Any]) -> None:
    if response is None:
        print("Failed to generate a response.")
        return

    message: str = response.choices[0].message.content
    for char in message:
        print(char, end="", flush=True)
        time.sleep(CHAR_DELAY)
    print()

    total_tokens: int = response.usage.total_tokens
    total_time: float = response.time_info.total_time
    tokens_per_second: float = total_tokens / total_time
    print(f"(Tokens per second: {tokens_per_second:.2f})")

def get_welcoming_text() -> str:
    return (
        f"\nWelcome to {MODEL_ID} Text Generator made by (Awan)\n"
        f"Happy chat and talk with your {MODEL_ID} AI Generative Model\n"
        "Addhe Warman Putra - (Awan)\n"
        "Type 'exit()' to exit from program\n"
    )

def main() -> None:
    try:
        client = setup_cerebras_client()
        chat_history: List[Dict[str, str]] = [SYSTEM_MESSAGE]

        print(get_welcoming_text())

        while True:
            user_input: str = input("> ")
            if user_input.lower() == "exit()":
                break

            response: Optional[Any] = generate_response(client, user_input, chat_history)
            if response:
                chat_history.append({
                    "role": "assistant",
                    "content": response.choices[0].message.content
                })
                print_response(response)
            else:
                print("Failed to generate a response. Please try again.")

    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Exiting...")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
