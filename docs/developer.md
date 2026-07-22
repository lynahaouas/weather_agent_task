# Weather Agent - Developer Documentation

## Architecture Overview
This project implements a simple LLM-based agent using the OpenAI-compatible 
function-calling (tool-calling) pattern, running against a local Ollama server.

## File Structure

- `src/weather_tool.py` — Handles all Open-Meteo API calls (geocoding + current temperature).
- `src/agent.py` — Core agent logic: system prompt, tool schema, and the LLM tool-calling loop.
- `src/logger_config.py` — Sets up logging to both console and timestamped log files.
- `src/main.py` — CLI entry point; creates the Ollama client and runs the agent.
- `run.sh` — Bash entrypoint; sets up the virtual environment, installs dependencies, and runs the agent.

## Design Decisions

- **Why raw OpenAI-style function calling instead of a framework (e.g., LangChain)**: 
  For a single-tool agent like this, using the native tool-calling API keeps the 
  reasoning flow fully transparent and easy to log/debug, without framework abstraction 
  hiding intermediate steps.

- **Why Qwen2.5 via Ollama**: Provides reliable native tool-calling support while running 
  fully locally, satisfying the requirement to run the environment locally without 
  external API dependencies.

- **Scope enforcement**: Handled primarily through a strict system prompt that explicitly 
  forbids answering any non-temperature question, including an exact refusal template, 
  since local models tend to need more explicit instruction reinforcement than larger 
  cloud models.

- **Two-stage geocoding + forecast lookup**: Open-Meteo's forecast API requires 
  coordinates, not city names, so `weather_tool.py` first resolves a city name to 
  latitude/longitude before requesting the current temperature.

## Extending This Project

To add more tools (e.g., weekly forecast, humidity), add a new function in 
`weather_tool.py`, describe it in the `TOOLS` schema in `agent.py`, and handle its 
name in the `if function_name == ...` block inside `run_agent()`.

## Logging

Each run generates a timestamped log file in `logs/`, capturing:
1. The user's question
2. The LLM's tool-call decision (if any) and arguments used
3. The tool's raw result
4. The final answer returned to the user