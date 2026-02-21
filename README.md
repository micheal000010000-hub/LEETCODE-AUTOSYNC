# 🍋 Lemonade Integration Branch  
## Offline AI-Powered LeetCode Workflow Engine

This branch integrates **Lemonade (local AI runtime)** into the existing LeetCode AutoSync system and introduces a backend abstraction layer for multi-runtime support and performance evaluation.

This project demonstrates how local LLM inference engines can power real-world developer workflows entirely offline.

---

# 🚀 Project Overview

This tool automates competitive programming workflows by:

- Generating structured LeetCode solution posts using local LLMs
- Managing repository structure automatically
- Sorting README entries intelligently
- Supporting asynchronous background generation (Producer–Consumer model)
- Allowing backend switching between inference engines
- Benchmarking runtime performance

Originally built with Ollama + Mistral, this branch adds:

- 🍋 Lemonade backend integration
- 🔄 Runtime abstraction layer
- 📊 Performance comparison module
- 🧪 Benchmark methodology documentation

---

# 🧠 Architecture Overview

```
User Input (CLI)
        ↓
autosync.py
        ↓
LLM Abstraction Layer (llm_generator.py)
        ↓
   ┌───────────────┬───────────────┐
   │               │               │
Ollama Backend   Lemonade Backend  (Extensible)
   │               │
Local Model     Local Model
   │               │
Structured Markdown Output
```

---

# 🔄 Multi-Backend Design

The system supports runtime switching via environment variable:

```
LLM_BACKEND=ollama
# or
LLM_BACKEND=lemonade
```

This abstraction ensures:

- Clean separation of concerns
- Extensibility for future runtimes
- Easy benchmarking across engines

---

# 🍋 Lemonade Integration

This branch integrates Lemonade as an alternative local inference backend.

Environment:

- OS: Windows 11
- GPU: AMD Radeon Graphics
- Lemonade installed locally
- Fully offline execution

The Lemonade backend is implemented inside:

```
llm_generator.py
```

as:

```
class LemonadeLLM(BaseLLM)
```

This backend mirrors the Ollama interface, ensuring compatibility with the existing system.

---

# ⚡ Performance Evaluation

This branch introduces runtime benchmarking to compare:

- Ollama vs Lemonade

## 📊 Metrics Measured

- Cold start latency
- Average inference latency (multiple runs)
- Response generation time
- Stability across repeated executions

## 🧪 Methodology

- Same prompt used for both backends
- Multiple runs executed
- Time measured using `time.perf_counter()`
- Averaged results documented

Example benchmarking snippet:

```python
import time

start = time.perf_counter()
response = llm.generate(prompt)
end = time.perf_counter()

latency = end - start
```

Results are documented in performance comparison tables.

---

# 🧵 Concurrency Model

The system uses a **Producer–Consumer architecture**:

- Main thread collects problem data
- Background worker processes LLM tasks
- `queue.Queue()` ensures thread-safe task handling
- `threading.Event()` enables graceful shutdown

This design prevents blocking during LLM generation.

---

# 📁 Project Structure

```
leetcode_autosync/
│
├── autosync.py
├── repo_manager.py
├── git_manager.py
├── llm_generator.py   # Backend abstraction + Lemonade integration
│
├── copy_paste_solution/
├── .env
├── requirements.txt
└── README.md
```

---

# 🌍 Why This Matters

Most AI-assisted workflows rely on cloud APIs.

This project demonstrates:

- Fully local LLM inference
- No cloud dependency
- Developer productivity automation
- Runtime-agnostic architecture
- Edge AI workflow engineering

It contributes to the local AI ecosystem by providing a reproducible example of integrating AI runtimes into real developer pipelines.

---

# 🔐 Configuration

Example `.env`:

```
LEETCODE_REPO_PATH=ABSOLUTE_PATH_TO_REPO
LLM_BACKEND=lemonade

# Ollama
OLLAMA_URL=http://localhost:11434/api/generate
MISTRAL_MODEL=mistral

# Lemonade
LEMONADE_URL=http://localhost:XXXX
LEMONADE_MODEL=model_name
```

---

# 🧪 Future Improvements

- GPU utilization measurement
- Token-per-second tracking
- Memory profiling
- UI layer (Streamlit/Gradio)
- Extended runtime benchmarking

---

# 📜 License

MIT License

---

# 🎯 Final Note

This branch represents an engineering experiment in:

- Runtime abstraction
- Local AI integration
- Edge-based inference workflows
- Developer productivity automation

Built to explore and demonstrate practical local AI system design.