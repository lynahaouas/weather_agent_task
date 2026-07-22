# Weather Agent - User Guide

A simple AI agent that answers questions about the current temperature of cities.

## Requirements

- Python 3.10+
- [Ollama](https://ollama.com) installed and running locally
- The `qwen2.5` model pulled in Ollama

## Setup

1. Clone this repository and navigate into it.
2. Make sure Ollama is running in the background.
3. Pull the required model (if not already done):
```bash
   ollama pull qwen2.5
```

## Running the Agent

Use the provided script, passing your question as an argument:

```bash
./run.sh "What's the temperature in Budapest right now?"
```

The first run will automatically set up a Python virtual environment and install dependencies. Subsequent runs will be faster.

## Example Usage

**Valid question:**
```bash
./run.sh "How hot is it in Vienna?"
```
Output:
The current temperature in Vienna, Austria, is 23.2 degrees Celsius.

**Off-topic question (will be declined):**
```bash
./run.sh "What is the capital of France?"
```
Output:
I can only answer questions about the current temperature of a city. Please ask me about a city's temperature.

## Logs

Every run creates a timestamped log file inside the `logs/` folder, recording each reasoning step (question received, tool called, tool result, final answer).