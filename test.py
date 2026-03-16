import subprocess
import json

result = subprocess.run(
    ["python", "run_current.py", "status"],
    capture_output=True,
    text=True
)

data = json.loads(result.stdout)

print("Total runs:", data["runs"]["total_runs"])
print("Prompt version:", data["prompt"]["current_prompt_version"])