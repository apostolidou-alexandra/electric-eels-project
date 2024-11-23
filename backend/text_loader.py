import app
import asyncio
import os

@app.post("/api/read_write")
async def read_and_write_file(file_path):
    try:

        with open(file_path, 'r') as file:
            content = file.read()

        commented = await app.add_comments(content)

        with open(file_path, 'w') as file:
            file.write(commented)

        return commented

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

# Function to process all code files in a repository
async def process_repository(repo_path, extensions):
    code_files = find_code_files(repo_path, extensions)
    print(code_files)
    tasks = [read_and_write_file(file) for file in code_files]
    await asyncio.gather(*tasks)



repo_path = "/home/sandra/repos/Repo-Search/repo-search/src"
extensions = [".py", ".js", ".java", ".c", ".cpp", ".tsx"]  

# Run the async function
asyncio.run(process_repository(repo_path, extensions))


