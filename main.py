import os
import time

import openai

# Define the model ID as a constant
MODEL_ID = "gpt-4o"


def setup_openai_api():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Missing OpenAI API Key.")
    openai.api_key = api_key


def generate_content(prompt: str, conversation_history: list):
    try:
        setup_openai_api()

        # Add new user prompt to the conversation history
        conversation_history.append({"role": "user", "content": prompt})

        response = openai.ChatCompletion.create(
            model=MODEL_ID,
            messages=conversation_history,
        )

        message = response['choices'][0]['message']["content"]

        # Add assistant's response to the conversation history
        conversation_history.append({"role": "assistant", "content": message})

        for char in message:
            print(char, end="", flush=True)
            time.sleep(0.02)
    except Exception as e:
        print(f"An error occurred: {e}")


def main(input_prompt=None):
    """Main function."""
    welcoming_text = f"""
    Welcome to {MODEL_ID} Text Generator made by (Awan),
    Happy chat and talk with your {MODEL_ID} AI Generative Model
    Addhe Warman Putra - (Awan)
    type 'exit()' to exit from program
    """
    print(welcoming_text)

    # Initialize conversation history with system message
    conversation_history = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

    if input_prompt is None:
        while True:
            prompt = input("\n> ")
            if prompt == "exit()":
                exit()
            generate_content(prompt, conversation_history)
    else:
        if input_prompt == "exit()":
            exit()
        generate_content(input_prompt, conversation_history)


if __name__ == "__main__":
    main()
