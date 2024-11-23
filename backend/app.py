from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from dotenv import load_dotenv
import openai
import os
from urllib.parse import urlparse
from openai import OpenAI

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("Missing OpenAI API key in environment variables.")

# Initialize OpenAI API
openai.api_key = OPENAI_API_KEY

# Initialize FastAPI app
app = FastAPI()

# Request model
class URL(BaseModel):
    url: str

# Validate URL function
def is_valid_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)
    except:
        return False

# Endpoint for processing prompt
@app.post("/api/prompt")
async def process_prompt(request: URL):
    prompt = "Create a UML diagram of this repo in PlantUML form. Only generate the PlantUML as text with no other text before or after."
    if not is_valid_url(request.url):
        raise HTTPException(status_code=400, detail="Invalid URL format.")

    try:
        client = OpenAI()
        completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": prompt + " " + request.url 
            }
            ]
        )

        reply = completion.choices[0].message

        return {"response": reply}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error with OpenAI API: {str(e)}")
    

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
