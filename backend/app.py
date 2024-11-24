from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from dotenv import load_dotenv
import openai
import os
from urllib.parse import urlparse
from openai import OpenAI
import uml_converter
import os

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
    prompt = "Create a greatly detailed UML diagram of this repo in PlantText UML form. Only generate the PlantUML as plain text (not encased in backticks) with no other text before or after."
    if not is_valid_url(request.url):
        raise HTTPException(status_code=400, detail="Invalid URL format.")

    try:
        client = OpenAI()
        completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a devoted, helpful and productive assistant."},
            {
                "role": "user",
                "content": prompt + " " + request.url 
            }
            ]
        )

        repo_path = "/home/sandra/repos/todo-list-python/" 
        process_repository(repo_path)

        reply = completion.choices[0].message.content

        uml_diagram = uml_converter.generate_uml_diagram(reply)

        return {"response": uml_diagram}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error with OpenAI API: {str(e)}")

def add_comments(file_content: str):
    prompt = "Add comments to this file of code where you deem necessary. Do not overdo it. Generate only the code wihtout any text before or after and without backticks surrounding it\n ``` \n" + file_content + "\n ```"

    try:
        client = OpenAI()
        completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a devoted, helpful and productive code commenter."},
            {
                "role": "user",
                "content": prompt
            }
            ]
        )

        reply = completion.choices[0].message.content
        return reply
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


def read_and_write_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()

        commented = add_comments(content)

        with open(file_path, 'w') as file:
            file.write(commented)

        return None

    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except IOError as e:
        print(f"An IOError occurred: {e}")
        return None



def find_code_files(repo_path, extensions):
    code_files = []
    for root, _, files in os.walk(repo_path):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                code_files.append(os.path.join(root, file))
    return code_files


extensions = [".py", ".js", ".java", ".c", ".cpp", ".tsx"] 

def process_repository(repo_path: str):
    try:
        code_files = find_code_files(repo_path, extensions)
        print(code_files)
        tasks = [read_and_write_file(file) for file in code_files]

        return {'code_files': code_files}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error with file commenting: {str(e)}")





