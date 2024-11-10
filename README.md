# Code Chat Server

The Code Chat Server is a FastAPI-based backend designed to integrate with Together AI's Llama models. It processes natural language prompts from users and returns AI-generated responses, facilitating real-time interaction with code models in development environments. The server supports conversational AI capabilities, enabling seamless integration with the Code Chat extension.

## Features

- **Multiple AI Model Integration**: Leverages Together AI's Llama models (Llama-3.2-11B, Meta-Llama-3.1-8B, CodeLlama-34B) to process natural language queries and generate accurate responses for general knowledge, optimization, and code-specific tasks.
  
- **Prompt Language Detection**: The server automatically detects the language of the user's prompt as part of the request processing. Responses are then generated in the detected language to provide contextually appropriate interactions, including code explanations and technical responses.

- **Historical Context Handling**: Supports conversation history, enabling the system to reference prior messages for more coherent, multi-turn interactions.

- **Real-time Interaction**: Responds to user queries in real-time, supporting dynamic use cases like debugging, code generation, and technical problem-solving.

## Future Work

- **Optimization**: Improve model response times and server efficiency.
- **Additional Models**: Extend support for additional AI models to enhance versatility and model selection.

## Project Structure

- **`src/app.py`**: Main FastAPI application file handling endpoints and CORS middleware.
- **`src/together_ai.py`**: Core logic for processing prompts, detecting language, interacting with models, and generating responses.
- **`dist.env`**: Template environment file. Copy to `.env` and add necessary environment variables.

## Requirements

- Python 3.8 or higher
- FastAPI, Together AI Llama SDK, dotenv, langdetect, and other dependencies listed in `requirements.txt`

## Setup Instructions

1. **Clone the Repository**:

   ```bash
   git clone git remote add origin git@github.com:ameentalahmeh/codechat-server.git
   cd codechat-server
   ```

2. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**:

   Copy `dist.env` to `.env` and update `TOGETHER_API_KEY` with your API key.

   ```bash
   cp dist.env .env
   ```

4. **Start the Server**:

   ```bash
   uvicorn src.app:app --reload
   ```

   The server will start at `http://127.0.0.1:8000`.

## Endpoints

- **`GET /`**: Home endpoint for server status.
- **`POST /api/prompt`**: Processes user prompts and returns generated responses from the AI model. Requires a JSON payload with `text`, and optionally `model` and `history`.

## Usage

To run the Code Chat extension locally with this server:

1. Ensure the **Code Chat Server** is up and running.
2. Start the extension's debug or test view in Visual Studio Code.
3. The extension will communicate with the server for prompt processing.
