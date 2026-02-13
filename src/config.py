import os
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY not set in .env file")
if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY not set in .env file")

MODEL = ChatAnthropic(model="claude-sonnet-4-5-20250929")

