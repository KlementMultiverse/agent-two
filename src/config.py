import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not set in .env file")
if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY not set in .env file")

# GPT-4o-mini for all agents — cheaper and better at structured output than Claude 3 Haiku
# Input: $0.15/MTok, Output: $0.60/MTok
MODEL = ChatOpenAI(model="gpt-4o-mini")
