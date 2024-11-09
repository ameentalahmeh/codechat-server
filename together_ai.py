import os
import logging
from llama_index.llms.together import TogetherLLM
from llama_index.core.llms import ChatMessage, MessageRole
from dataclasses import dataclass
from dotenv import load_dotenv
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

# Load environment variables early on
load_dotenv()

# Check if the necessary environment variable is present
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
if not TOGETHER_API_KEY:
    log.error("TOGETHER_API_KEY is not set in the environment variables.")
    raise ValueError("TOGETHER_API_KEY is required but not found.")

# Dataclass to hold function input
@dataclass
class FunctionInputParams:
    prompt: str

# Singleton to reuse the TogetherLLM instance
class LLMClient:
    _instance: Optional[TogetherLLM] = None

    @classmethod
    def get_instance(cls) -> TogetherLLM:
        """Return the singleton instance of the LLM client."""
        if cls._instance is None:
            cls._instance = TogetherLLM(
                model="codellama/CodeLlama-34b-Instruct-hf", api_key=TOGETHER_API_KEY
            )
        return cls._instance

# function to process the prompt
def process_prompt(input: FunctionInputParams):
    try:
        log.debug(f"Processing prompt: {input.prompt}")

        # Get the LLM client instance
        llm = LLMClient.get_instance()

        # Prepare the messages for the LLM chat
        messages = [
            ChatMessage(
                role=MessageRole.SYSTEM, 
                content="You are a pirate with a colorful personality"
            ),
            ChatMessage(role=MessageRole.USER, content=input.prompt),
        ]

        # Perform the chat operation (assuming chat() is async)
        resp = llm.chat(messages)
        return resp.message.content

    except ConnectionError as e:
        log.error(f"Connection error when interacting with LLM: {e}")
    except TimeoutError as e:
        log.error(f"Timeout error when interacting with LLM: {e}")
    except Exception as e:
        log.error(f"Unexpected error: {e}")
