"""
main.py
Command-line entry point for the weather agent.
Usage: python -m src.main "What's the temperature in Budapest?"
"""

import sys
from openai import OpenAI
from src.logger_config import setup_logger
from src.agent import run_agent


def main():
    logger = setup_logger()

    if len(sys.argv) < 2:
        print("Usage: python -m src.main \"<your question>\"")
        sys.exit(1)

    user_question = sys.argv[1]

    client = OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama",  
    )

    answer = run_agent(user_question, client, model="qwen2.5")

    print("\n--- FINAL ANSWER ---")
    print(answer)


if __name__ == "__main__":
    main()