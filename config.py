import os
from dotenv import load_dotenv

load_dotenv()

LEETCODE_REPO_PATH = os.getenv("LEETCODE_REPO_PATH")

if not LEETCODE_REPO_PATH:
    raise ValueError("LEETCODE_REPO_PATH not set in .env file")