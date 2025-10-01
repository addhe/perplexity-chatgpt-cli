# config.py
import os

# Model configuration
MODEL_ID = os.getenv("PERPLEXITY_MODEL", "llama-3.1-sonar-small-128k-online")

# API configuration
API_KEY = os.getenv("PERPLEXITY_API_KEY")

# Application configuration
CHAR_DELAY = float(os.getenv("CHAR_DELAY", "0.02"))
