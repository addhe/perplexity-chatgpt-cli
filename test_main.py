import sys
import unittest
from io import StringIO
from unittest.mock import patch

import openai

from main import generate_content, main, setup_openai_api


class TestMain(unittest.TestCase):

    def setUp(self):
        self.api_key_patcher = patch.object(openai, 'api_key', 'fake-api-key')
        self.api_key_patcher.start()

        self.model_patcher = patch(
            'openai.ChatCompletion.create', return_value={
                'choices': [{
                    'message': {'content': 'This is a fake response from the OpenAI API.'}
                }]
            })
        self.mock_create = self.model_patcher.start()

    def tearDown(self):
        patch.stopall()

    def test_main(self):
        captured_output = StringIO()
        sys.stdout = captured_output

        main(input_prompt="Hello, world!")

        sys.stdout = sys.__stdout__

        actual_output = captured_output.getvalue().strip()
        # Debug step to see the actual output
        print(f"Captured Output:\n{actual_output}")

        expected_output_start = """
        Welcome to gpt-4o Text Generator made by (Awan),
        Happy chat and talk with your gpt-4o AI Generative Model
        Addhe Warman Putra - (Awan)
        type 'exit()' to exit from program
        """.strip()

        # Normalize both strings to ignore leading/trailing whitespace
        actual_lines = [line.strip() for line in actual_output.splitlines()]
        expected_lines = [line.strip()
                          for line in expected_output_start.splitlines()]

        for expected_line in expected_lines:
            self.assertIn(expected_line, actual_lines)

        # Ensure the response is in the actual output
        self.assertIn(
            "This is a fake response from the OpenAI API.", actual_output)

    @patch('main.os.getenv', return_value='fake-api-key')
    def test_setup_openai_api(self, mock_getenv):
        setup_openai_api()
        self.assertEqual(openai.api_key, "fake-api-key")

    def test_generate_content(self):
        result = generate_content("Hello, world!")
        self.assertEqual(result, None)

        self.mock_create.assert_called_once_with(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello, world!"},
            ]
        )


if __name__ == "__main__":
    unittest.main()
