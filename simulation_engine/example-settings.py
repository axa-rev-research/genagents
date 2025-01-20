from pathlib import Path

OPENAI_API_KEY = "API_KEY"
KEY_OWNER = "NAME"

DEBUG = False

MAX_CHUNK_SIZE = 4

LLM_VERS = "gpt-4o-mini"

USE_AZURE_LLMS = True
USE_AZURE_EMBEDDINGS=True
AZURE_OPENAI_ENDPOINT = "ENDPOINT"
AZURE_OPENAI_API_KEY = "API_KEY"
# For the LLM model, we use the same variable LLM_VERS even when using Azure
AZURE_EMBEDDING_MODEL="text-embedding-3-small"
AZURE_MODEL_API_VERSION = "2024-08-01-preview" # for gp4-4o-mini
AZURE_EMBEDDING_MODEL_API_VERSION = "2023-05-15"

BASE_DIR = f"{Path(__file__).resolve().parent.parent}"

## To do: Are the following needed in the new structure? Ideally Populations_Dir is for the user to define.
POPULATIONS_DIR = f"{BASE_DIR}/agent_bank/populations" 
LLM_PROMPT_DIR = f"{BASE_DIR}/simulation_engine/prompt_template"