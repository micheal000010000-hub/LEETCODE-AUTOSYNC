# 🚀 LeetCode AutoSync with Mistral (via Ollama)

Automate your LeetCode workflow like a professional. This README has been updated to use the Mistral model (run locally via `ollama` or via hosted Mistral endpoints) instead of Gemini.

This tool helps you:

- ✅ Add new LeetCode solutions locally (organized by difficulty)
- ✅ Automatically update your main LeetCode repository README (sorted numerically)
- ✅ Generate a fully structured LeetCode Solution Post using **Gemini 2.5 Flash**
- ✅ Instantly copy-paste AI-generated content into LeetCode “Solutions” section
- ✅ Push changes to GitHub with a formatted date-based commit message
- ✅ Keep generated solution posts separate and excluded from Git tracking

---

# ✨ Why This Exists

When practicing LeetCode daily, the repetitive tasks become exhausting:

- Creating new files manually
- Adding headers
- Updating README
- Sorting entries
- Writing solution explanations
- Formatting markdown properly
- Committing and pushing to GitHub

This tool automates all of it.

It lets you focus on solving problems — not managing files.

---

# 🧠 What This Tool Does

When you run:

```
python autosync.py
```

You get two options:

```
1 → Add new solution locally + Generate AI solution post
2 → Push existing changes to GitHub
```

---

## 🔹 Option 1 — Add New Solution + Generate AI Post

You provide:

- Problem number
- Problem name
- Difficulty (easy / medium / hard)
- Problem link
- Your Python solution

The tool then:

### 1️⃣ Creates the solution file

Inside your LeetCode repository:

```
easy/
medium/
hard/
```

With proper formatting:

```python
"""
LeetCode 506_Relative Ranks
Difficulty: Easy
Link: https://leetcode.com/...
"""
```

---

### 2️⃣ Updates README.md

- Inserts the solution under the correct difficulty section
- Sorts entries numerically (e.g., 1, 2, 506)
- Prevents duplicates

---

### 3️⃣ Calls an LLM (Mistral via Ollama or hosted)

It generates a structured solution post using a Mistral model (local via `ollama` or a hosted Mistral API) and includes:

- A professional, descriptive title  
  (e.g., "O(n) HashMap-Based Python Solution | Clean Approach")
- ## Intuition
- ## Approach
- ## Time Complexity
- ## Space Complexity
- ## Code (formatted with ```python3)

You can directly copy-paste it into LeetCode’s **Solutions** section.

---

### 4️⃣ Saves AI Output Locally

Inside:

```
leetcode_autosync/
└── copy_paste_solution/
```

This folder:

- Is automatically cleared before every run
- Always contains only ONE fresh structured solution
- Is ignored by Git

---

## 🔹 Option 2 — Push to GitHub

Runs:

```
git add .
git commit -m "commit_DD_MM_YYYY"
git push -f
```

Using today's date automatically.

---

# 🤖 AI Model Used

This project is configured to use Mistral models. You can run Mistral locally via `ollama` (recommended for offline/local development) or use a hosted Mistral endpoint (for managed inference).

Example model: `mistralai/mistral-7b` (or any other Mistral model tag supported by your runtime). The repository code expects an LLM endpoint; see the *Configuration* section for environment variables.

Why Mistral?

- Strong technical writing for concise explanations
- Efficient inference for local heavyweight models
- Good open-source model options for offline usage

---

# 📁 Project Structure

```
leetcode_autosync/
│
├── autosync.py              # Main CLI entry point
├── config.py                # Loads environment variables
├── repo_manager.py          # File creation + README updates
├── git_manager.py           # Git automation
├── llm_generator.py         # Gemini 2.5 Flash integration
│
├── copy_paste_solution/     # Auto-cleared AI output folder (ignored by git)
│
├── .env                     # Environment variables (NOT committed)
├── .gitignore
├── requirements.txt
└── README.md
```

---

# 📂 Required Structure of Your LeetCode Repository

Your main LeetCode repo must look like this:

```
LeetCode Solutions/
│
├── easy/
├── medium/
├── hard/
└── README.md
```

Your README must contain sections:

```
## Easy
## Medium
## Hard
```

The tool will:

- Insert new entries
- Keep them sorted
- Avoid duplicates

---

# 🔐 .env Configuration

Create a `.env` file inside `leetcode_autosync/`:

```
LEETCODE_REPO_PATH=ABSOLUTE_PATH_TO_YOUR_LEETCODE_REPO
# If using local Ollama (default example):
OLLAMA_URL=http://localhost:11434
MISTRAL_MODEL=mistralai/mistral-7b

# If using a hosted Mistral API instead of Ollama, set:
# MISTRAL_API_KEY=your_hosted_mistral_api_key
# MISTRAL_API_URL=https://api.mistral.ai/v1
```

Example (Windows):

```
LEETCODE_REPO_PATH=C:/Users/YourName/Documents/LeetCode Solutions
OLLAMA_URL=http://localhost:11434
MISTRAL_MODEL=mistralai/mistral-7b
```

---

# 📦 requirements & dependencies

The project uses `python-dotenv` for configuration. If you will call a local `ollama` HTTP API, ensure you have `requests` installed as well.

Recommended `requirements.txt` entries:

```
python-dotenv
requests
```

Install:

```
pip install -r requirements.txt
```

If you previously used `google-genai` for Gemini, remove or ignore it when switching to Ollama-based Mistral usage unless you still plan to use Gemini.

---

# 🚫 .gitignore

```
.env
__pycache__/
*.pyc
copy_paste_solution/
```

---

# 🛠 How It Works (High-Level Architecture)

```
You
  ↓
autosync.py (CLI)
  ↓
repo_manager.py
  ↓
Updates LeetCode Repo
  ↓
llm_generator.py
  ↓
Mistral model (local via Ollama or hosted Mistral API)
  ↓
Structured Markdown Output
  ↓
Saved in copy_paste_solution/
```

---

## ✅ Running Mistral locally with Ollama (detailed)

This project supports running Mistral models locally using the `ollama` runtime which exposes a simple HTTP API by default on `http://localhost:11434`.

1) Install prerequisites

- macOS: Install via Homebrew (recommended):

  ```bash
  brew install ollama
  ```

- Linux: Use the official install script (check https://ollama.com/docs/install for the latest):

  ```bash
  curl -sSf https://ollama.com/install.sh | sh
  ```

- Windows: Use WSL2 (Ubuntu) or Docker. Recommended flow:

  - Install WSL2 and an Ubuntu distro from the Microsoft Store.
  - Inside WSL, follow the Linux install steps above.
  - Alternatively, run `ollama` inside Docker if you prefer containerized usage.

2) Start or verify `ollama`

After installation, verify the daemon is running and reachable:

```bash
ollama --version
ollama list   # shows downloaded models
```

If `ollama` provides a system service, ensure it is running. Otherwise starting `ollama` is typically automatic on first command.

3) Pull a Mistral model

Find the exact model tag in the Ollama model registry or your preferred model registry. Example (replace with the correct tag):

```bash
ollama pull mistralai/mistral-7b
```

You can list models with:

```bash
ollama list
```

4) Test the model via the HTTP API

Basic `curl` test (replace `mistralai/mistral-7b` if needed):

```bash
curl -s -X POST "http://localhost:11434/api/generate" \
  -H "Content-Type: application/json" \
  -d '{"model":"mistralai/mistral-7b","prompt":"Explain quicksort in two sentences."}'
```

Example Python usage (simple request):

```python
import os
import requests

ollama_url = os.getenv('OLLAMA_URL', 'http://localhost:11434')
model = os.getenv('MISTRAL_MODEL', 'mistralai/mistral-7b')

resp = requests.post(
    f"{ollama_url}/api/generate",
    json={"model": model, "prompt": "Write a short explanation of Dijkstra's algorithm."},
)
print(resp.json())
```

5) Integrate with this project

- Set `OLLAMA_URL` and `MISTRAL_MODEL` in your `.env`.
- Update `llm_generator.py` (or your LLM wrapper) to call `OLLAMA_URL/api/generate` using `requests` and use the `MISTRAL_MODEL` name when generating prompts.

---

## ✅ Using Hosted Mistral APIs

If you prefer a hosted Mistral service (instead of local Ollama), set `MISTRAL_API_URL` and `MISTRAL_API_KEY` in `.env`. The calling pattern depends on the hosted provider's API (refer to their docs). Typical steps:

1. Obtain an API key from the hosted provider.
2. Put `MISTRAL_API_KEY` and `MISTRAL_API_URL` in `.env`.
3. Update `llm_generator.py` to send requests to the provider's endpoint with the API key.

---

If you want, I can also open `llm_generator.py` and provide a compact example that calls `ollama`'s HTTP API directly. Would you like that?

Clean separation of responsibilities.

---

# 🎯 Who Is This For?

- Students practicing LeetCode daily
- Developers building public GitHub consistency
- Anyone wanting automated structured solution posts
- Learners who want to focus on problem-solving, not formatting

---

# 💡 Why This Is Powerful

You now have:

- Repository automation
- AI-assisted explanation writing
- Proper markdown formatting
- Organized solution tracking
- One-command GitHub publishing
- A reproducible workflow system

This is not just automation.

It is workflow engineering.

---

# 🧩 Future Improvements (Optional Ideas)

- Auto-copy generated markdown to clipboard
- Auto-open LeetCode submission page
- Auto-update “Last Updated” timestamp in README
- Auto-detect duplicate problem entries
- Add colored CLI output
- Add logging system
- Add statistics dashboard

---

# 🤝 Contributions

Contributions are welcome!

If you'd like to:

- Improve prompt quality
- Enhance formatting
- Add model selection
- Improve README parsing
- Add UI layer
- Add test coverage

Feel free to open a Pull Request.

---

# 📜 License

This project is open for educational and personal use.

---

# ⭐ Final Note

Consistency is more important than intensity.

Automate the boring.
Focus on solving.
Ship daily.
Stay consistent.

Happy Coding 🚀