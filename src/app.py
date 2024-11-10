from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.together_ai import process_prompt, UserPrompt

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
    return {"message": "Welcome to the Code Chat API!"}

@app.post("/api/prompt")
def process_prompt_endpoint(request: UserPrompt):
    try:
        result = process_prompt(request)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
