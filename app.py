from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dataclasses import dataclass
from together_ai import process_prompt

# Define request model
@dataclass
class PromptRequest:
    prompt: str
    model: str = "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"
    # model: str = "codellama/CodeLlama-34b-Instruct-hf"
    # model: str = "codellama/CodeLlama-7b-hf"

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def home():
    return {"message": "Welcome to the TogetherAI LlamaIndex FastAPI App!"}

@app.post("/api/prompt")
def process_prompt_endpoint(request: PromptRequest):
    try:
        result = process_prompt(request)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
