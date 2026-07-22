"""
agent.py
Core agent logic: takes a user question, uses an LLM with function-calling
to decide whether to fetch weather data, executes the tool if needed,
and returns a final natural-language answer.
"""

import json
import logging
from openai import OpenAI
from src.weather_tool import get_city_temperature

logger = logging.getLogger("weather_agent")

SYSTEM_PROMPT = (
    "You are a weather assistant with ONE job: reporting the current temperature "
    "of cities that the user names. You must NOT answer any other type of question, "
    "even if you know the answer. This includes general knowledge, geography, math, "
    "or any topic unrelated to current city temperature.\n\n"
    "If the user asks anything other than a city's current temperature, respond with "
    "EXACTLY this and nothing else: "
    "\"I can only answer questions about the current temperature of a city. "
    "Please ask me about a city's temperature.\"\n\n"
    "Do not explain, do not add extra information, do not answer the off-topic part "
    "of the question even partially."
)

# This schema describes our tool to the LLM - its name, purpose, and expected arguments
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_city_temperature",
            "description": "Get the current temperature for a specific city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city_name": {
                        "type": "string",
                        "description": "The name of the city, e.g. 'Budapest' or 'Vienna'",
                    }
                },
                "required": ["city_name"],
            },
        },
    }
]


def run_agent(user_question: str, client: OpenAI, model: str = "qwen2.5") -> str:
    logger.info(f"User question: {user_question}")

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_question},
    ]

    # Step 1: Ask the LLM what to do - answer directly or call a tool
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=TOOLS,
    )

    message = response.choices[0].message

    # Step 2: Check if the LLM decided to call our tool
    if message.tool_calls:
        for tool_call in message.tool_calls:
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            logger.info(f"LLM decided to call tool: {function_name} with args: {arguments}")

            if function_name == "get_city_temperature":
                tool_result = get_city_temperature(arguments["city_name"])
                logger.info(f"Tool result: {tool_result}")
            else:
                tool_result = {"error": f"Unknown function: {function_name}"}

            # Step 3: Send the tool result back to the LLM so it can form a final answer
            messages.append(message)
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(tool_result),
                }
            )

        final_response = client.chat.completions.create(
            model=model,
            messages=messages,
        )
        final_answer = final_response.choices[0].message.content
    else:
        # LLM answered directly without needing a tool (e.g., declined an off-topic question)
        final_answer = message.content

    logger.info(f"Final answer: {final_answer}")
    return final_answer