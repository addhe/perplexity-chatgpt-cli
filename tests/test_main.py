import unittest
from unittest.mock import patch, MagicMock
import time
from typing import Any, List, Dict, Optional
import os
import sys

from cerebras.cloud.sdk import Cerebras

import src.main as main_module
from config import MODEL_ID, SYSTEM_MESSAGE, API_KEY, CHAR_DELAY

class TestMainModule(unittest.TestCase):

    def setUp(self):
        # Reset the cerebras_client before each test
        main_module.cerebras_client = None

    @patch('src.main.Cerebras')
    def test_setup_cerebras_client(self, mock_cerebras: MagicMock) -> None:
        """Test that setup_cerebras_client returns the existing client correctly."""
        client = main_module.setup_cerebras_client()
        mock_cerebras.assert_not_called()  # Cerebras constructor should not be called
        self.assertIs(client, main_module.cerebras_client)


    @patch('builtins.print')
    @patch('time.sleep')
    def test_print_response(self, mock_sleep: MagicMock, mock_print: MagicMock):
        """Test that print_response prints the response with a delay."""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content="This is a test response."))]
        mock_response.usage = MagicMock(total_tokens=20)
        mock_response.time_info = MagicMock(total_time=0.5)

        main_module.print_response(mock_response)
        self.assertEqual(mock_print.call_count, 26)
        self.assertEqual(mock_sleep.call_count, 24)

    @patch('src.main.setup_cerebras_client')
    def test_generate_response(self, mock_setup: MagicMock) -> None:
        """Test that generate_response interacts with the Cerebras client correctly."""
        mock_client = MagicMock()
        mock_setup.return_value = mock_client
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content="Generated text"))]
        mock_client.chat.completions.create.return_value = mock_response

        prompt = "This is a test prompt."
        chat_history = [SYSTEM_MESSAGE]
        response = main_module.generate_response(mock_client, prompt, chat_history)

        mock_client.chat.completions.create.assert_called_once_with(
            messages=chat_history,
            model=MODEL_ID,
        )
        self.assertEqual(response, mock_response)


    def test_get_welcoming_text(self):
        """Test that get_welcoming_text returns the expected text."""
        expected_text = (
            f"\nWelcome to {MODEL_ID} Text Generator made by (Awan)\n"
            f"Happy chat and talk with your {MODEL_ID} AI Generative Model\n"
            "Addhe Warman Putra - (Awan)\n"
            "Type 'exit()' to exit from program\n"
        )
        self.assertEqual(main_module.get_welcoming_text(), expected_text)

if __name__ == '__main__':
    unittest.main()
