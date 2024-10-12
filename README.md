# Cerebras AI Chat Application
This is a Python-based chat application that uses the Cerebras AI model to generate responses. It allows users to interact with a large language model in a conversational manner.

## Features
* Utilizes the Cerebras LLaMA 3.1 70B model
* Interactive command-line interface
* Real-time response generation
* Performance metrics display (tokens per second)
* Typewriter-style output for responses

## Prerequisites
* Python 3.6+
* Cerebras Cloud SDK
* Cerebras API Key

## Installation
1. Clone this repository or download the main.py file.
2. Install the required dependencies:
```
pip install cerebras-cloud-sdk
```
3. Set up your Cerebras API Key as an environment variable:
```
export CEREBRAS_API_KEY=your_api_key_here
```

# Usage
Run the script using Python:
```
python main.py
```

* The application will start and display a welcome message.
* Enter your prompts at the > prompt.
* The AI will generate and display responses.
* Type exit() to quit the application.

# Code Structure
* ```setup_cerebras_client()```: Sets up the Cerebras client using the API key.
* ```generate_response()```: Generates a response using the Cerebras model.
* ```print_response()```: Prints the AI's response with a typewriter effect and displays performance metrics.
* ```main()```: The main function that runs the chat loop.

# Author
Addhe Warman Putra (Awan)

# License
This project is open-source and available under the MIT License.

# Disclaimer
This application requires a valid Cerebras API key and access to the Cerebras Cloud platform. Make sure you have the necessary permissions and subscriptions before using this application.