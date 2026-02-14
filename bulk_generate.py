import os
import re
import time
import gc
from tqdm import tqdm
from dotenv import load_dotenv
import requests
from config import LEETCODE_REPO_PATH

TARGET_DIFFICULTY = "medium"
OLLAMA_MODEL = "mistral"  # Change if needed
OLLAMA_URL = "http://localhost:11434/api/generate"

load_dotenv()


def extract_metadata_and_code(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract from docstring at top
    number_match = re.search(r"LeetCode\s+(\d+)", content)
    difficulty_match = re.search(r"Difficulty:\s+(\w+)", content)
    link_match = re.search(r"Link:\s+(https?://\S+)", content)

    if not number_match:
        print(f"⚠️  Skipping {file_path} — no LeetCode number found")
        return None

    problem_number = number_match.group(1)
    difficulty = difficulty_match.group(1) if difficulty_match else "Unknown"
    link = link_match.group(1).strip() if link_match else ""

    filename = os.path.basename(file_path)
    name_part = re.sub(r"^\d+_?-?\s*", "", filename).replace(".py", "").strip()
    problem_name = name_part

    # Extract code AFTER the closing """ of the docstring
    docstring_end = content.find('"""', content.find('"""') + 1)
    solution_code = content[docstring_end + 3:].strip()

    if not solution_code:
        print(f"⚠️  Skipping {file_path} — no solution code found")
        return None

    return problem_number, problem_name, difficulty, link, solution_code


def generate_solution_ollama(problem_number, problem_name, difficulty, link, code):
    prompt = f"""You are an expert technical writer.

Problem: {problem_number} — {problem_name}
Difficulty: {difficulty}
Link: {link}

Python Solution:
{code}

Generate structured Markdown with:
1. SHORT technical title (max 10 words) mentioning technique, time complexity, Python
2. Sections: Intuition, Approach, Time Complexity, Space Complexity, Code

Keep it concise and professional."""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "num_predict": 800,  # Limit output tokens to speed things up
                "prompt": prompt,
                "stream": False,
                "temperature": 0.2,
            },
            timeout=600,
        )

        if response.status_code == 200:
            return response.json()["response"].strip()
        else:
            return None

    except requests.exceptions.Timeout:
        return "TIMEOUT_ERROR"
    except requests.exceptions.ConnectionError:
        return "OLLAMA_NOT_RUNNING"
    except Exception as e:
        return f"ERROR: {str(e)}"


def main():
    output_folder = os.path.join(os.getcwd(), "bulk_generated_posts_ollama")
    os.makedirs(output_folder, exist_ok=True)

    folder_path = os.path.join(LEETCODE_REPO_PATH, TARGET_DIFFICULTY)

    if not os.path.exists(folder_path):
        print(f"❌ Folder not found: {folder_path}")
        return

    files = [f for f in sorted(os.listdir(folder_path)) if f.endswith(".py")]

    print(f"\n🚀 Processing {TARGET_DIFFICULTY.upper()} ({len(files)} files)")
    print(f"🤖 Model: {OLLAMA_MODEL}\n")

    generated = 0
    skipped = 0
    failed = 0
    metadata_failed = 0

    for idx, file in enumerate(files, 1):
        file_path = os.path.join(folder_path, file)
        data = extract_metadata_and_code(file_path)

        if not data:
            print(f"[{idx}/{len(files)}] ⏭️  SKIPPED: {file} — metadata extraction failed")
            metadata_failed += 1
            skipped += 1
            continue

        problem_number, problem_name, diff, link, code = data
        output_file = os.path.join(output_folder, f"{problem_number}_{problem_name}.md")

        if os.path.exists(output_file):
            print(f"[{idx}/{len(files)}] ⏭️  SKIPPED: Problem {problem_number} — already exists")
            skipped += 1
            continue

        print(f"[{idx}/{len(files)}] 🔄 Processing: Problem {problem_number} — {problem_name}...", end=" ", flush=True)

        result = generate_solution_ollama(problem_number, problem_name, diff, link, code)

        if result == "OLLAMA_NOT_RUNNING":
            print(f"\n\n❌ OLLAMA NOT RUNNING!")
            print(f"Start it with: ollama serve")
            print(f"Then run this script again.\n")
            return

        elif result == "TIMEOUT_ERROR":
            print(f"❌ TIMEOUT (model took too long)")
            failed += 1

        elif result and not result.startswith("ERROR"):
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(result)
            print(f"✅ SUCCESS")
            generated += 1

        else:
            print(f"❌ FAILED: {result}")
            failed += 1

        # Clear memory after each file
        gc.collect()
        time.sleep(2)

    # Print final summary ONCE at the end
    print(f"\n{'='*60}")
    print(f"FINAL RESULTS:")
    print(f"{'='*60}")
    print(f"✅ Generated        : {generated}")
    print(f"⏭️  Skipped (exists) : {skipped - metadata_failed}")
    print(f"⚠️  Metadata failed  : {metadata_failed}")
    print(f"❌ Failed           : {failed}")
    print(f"📂 Output folder    : {output_folder}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()