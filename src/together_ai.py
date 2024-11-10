import os
import logging
from dataclasses import dataclass, field
from llama_index.llms.together import TogetherLLM
from llama_index.core.llms import ChatMessage, MessageRole
from dataclasses import dataclass
from dotenv import load_dotenv
from typing import Optional
from langdetect import detect

# Configure logging
logLevel = logging.ERROR if os.getenv("ENV") == "prod" else logging.INFO
logging.basicConfig(level=logLevel, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

# Load environment variables early on
load_dotenv()

# Check if the necessary environment variable is present
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
if not TOGETHER_API_KEY or TOGETHER_API_KEY == "":
    log.error("TOGETHER_API_KEY is not set in the environment variables.")
    raise ValueError("TOGETHER_API_KEY is required but not found.")

# Dataclass to hold function input
@dataclass
class UserPrompt:
    text: str
    model: str = "meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo"
    history: list = field(default_factory=list)

# Singleton to reuse the TogetherLLM instance
class LLMClient:
    _instance: Optional[TogetherLLM] = None

    @classmethod
    def get_instance(cls, model: str) -> TogetherLLM:
        """Return the singleton instance of the LLM client."""
        if cls._instance is None or cls._instance.model != model:
            # Ensure model is a valid string, fallback if it's not provided or invalid
            cls._instance = TogetherLLM(
                model=model, api_key=TOGETHER_API_KEY
            )
        return cls._instance

# Function to determine the system message without added personality tone
def get_system_message(language: str) -> str:
    return (
        f"Please use the user's language ({language}) for non-code explanations, and don't append notes in the bottom. Finally, format the code clearly in markdown."
    )


# Function to process the prompt and clean up the response
def process_prompt(input: UserPrompt):
    try:
        log.info(f"Processing prompt: {input.text}")

        # Detect the language of the user's input
        language = detect(input.text)
        log.info(f"Detected language: {language}")

        # Get the system message without any tone customization
        system_message = get_system_message(language)

        # Get request model
        model = input.model
        log.info(f"Detected model: {model}")

        # Get the LLM client instance
        llm = LLMClient.get_instance(model)

        # Prepare the messages for the LLM chat
        messages = [
            ChatMessage(role=MessageRole.SYSTEM, content=system_message),
            ChatMessage(role=MessageRole.USER, content=f"Please provide full description and code samples for '{input.text}'."),
        ]

        # Append History messages
        if len(input.history) > 0:
            for h in input.history:
                messages.append(ChatMessage(role=h['role'], content=h['content']))

        # Perform the chat operation
        resp = llm.chat(messages)

        # Raw response
        result = resp.message.content

        return result
    except ConnectionError as e:
        log.error(f"Connection error when interacting with LLM: {e}")
    except TimeoutError as e:
        log.error(f"Timeout error when interacting with LLM: {e}")
    except Exception as e:
        log.error(f"Unexpected error: {e}")
