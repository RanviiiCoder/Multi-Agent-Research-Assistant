import os
from huggingface_hub import HfApi, create_repo
from dotenv import load_dotenv

load_dotenv()

# The HF Token from environment
HF_TOKEN = os.getenv("HF_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
REPO_NAME = "Multi-Agent-Research-Assistant"

api = HfApi(token=HF_TOKEN)

try:
    print("Creating Space on Hugging Face...")
    # This creates a Docker space
    repo_url = create_repo(
        repo_id=REPO_NAME,
        repo_type="space",
        space_sdk="docker",
        private=False,
        token=HF_TOKEN,
        exist_ok=True
    )
    repo_id = repo_url.repo_id
    print(f"Space created/found at: {repo_url}")
    
    print("Uploading files to Space...")
    # Upload everything except venv and env files
    api.upload_folder(
        folder_path=".",
        repo_id=repo_id,
        repo_type="space",
        ignore_patterns=["venv/*", ".env", ".venv", ".git/*", "__pycache__/*", "deploy_hf.py"]
    )
    
    print("Adding GEMINI_API_KEY as a secret...")
    api.add_space_secret(
        repo_id=repo_id,
        key="GEMINI_API_KEY",
        value=GEMINI_API_KEY
    )
    
    print(f"Deployment successfully initiated! View your Space at: https://huggingface.co/spaces/{repo_id}")
    
except Exception as e:
    print(f"An error occurred during deployment: {e}")
