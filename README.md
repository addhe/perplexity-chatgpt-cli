# GPT-4o Text Generator

Addhe Warman Putra (Awan) Personal OpenAI ChatGPT on Linux Terminal.

This project showcases the capabilities of the GPT-4o model, a large language model, for generating human-like text.

## Features

* Generate text based on a given prompt.
* Interactive command-line interface for easy user interaction.
* Welcome message and instructions to guide users.

## Setup

To use this script, you will need the following:

* OpenAI API key (obtainable from OpenAI website)
* Python 3.8 or later
* Virtual environment (recommended)

## Usage


1. Clone the repository:
`$ git clone https://github.com/awanwb/gpt-4o-text-generator.git`
2. Create a virtual environment and activate it:
   ```
   $ python3 -m venv venv 
   $ source venv/bin/activate
   ```
3. Install dependencies:
   `$ pip install -r requirements.txt`
4. Set your OpenAI API key in the environment:
   `$ export OPENAI_API_KEY=<your_openai_api_key>`
5. Run the script:
   `$ python main.py`

## Example
   After launching the script, you will be greeted with a welcome message and instructions. You can then type prompts and the model will generate text based on your input. For example:

```
> What is the meaning of life?
> The meaning of life is a deeply personal question that has been pondered by philosophers and thinkers for centuries. There is no one definitive answer, but some common themes that emerge include finding purpose and fulfillment in relationships, work, creativity, and personal growth.
```

## Exit
```
> To exit the script, type exit() at the prompt.
```

Notes
* The model may take some time to generate text, especially for longer prompts.
* The generated text may not always be accurate or factual.
* Use the model responsibly and respectfully.
