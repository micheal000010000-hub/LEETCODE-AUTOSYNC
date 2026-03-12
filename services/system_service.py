import os
import sqlite3
from typing import Any, Dict, List

import requests

from config import OLLAMA_BASE_URL, OLLAMA_MODEL, PROMPT_VERSION
from services.metrics_service import get_metrics_paths


def check_ollama_health(timeout_seconds: int = 4) -> Dict[str, str]:
    tags_url = f"{OLLAMA_BASE_URL}/api/tags"
    try:
        response = requests.get(tags_url, timeout=timeout_seconds)
        if response.status_code != 200:
            return {
                "reachable": "False",
                "message": f"Ollama reachable but returned {response.status_code}",
                "model_loaded": "Unknown",
                "models": "",
            }

        payload = response.json() if response.content else {}
        models_payload: List[Dict] = payload.get("models", [])
        model_names = [m.get("name", "") for m in models_payload if isinstance(m, dict)]
        target_present = any(OLLAMA_MODEL in name for name in model_names)

        return {
            "reachable": "True",
            "message": "Ollama is reachable",
            "model_loaded": str(target_present),
            "models": ", ".join(model_names[:8]),
        }

    except requests.exceptions.Timeout:
        return {
            "reachable": "False",
            "message": "Connection timed out",
            "model_loaded": "Unknown",
            "models": "",
        }
    except requests.exceptions.RequestException as exc:
        return {
            "reachable": "False",
            "message": f"Connection failed: {str(exc)}",
            "model_loaded": "Unknown",
            "models": "",
        }


def get_project_runtime_snapshot() -> Dict[str, str]:
    paths = get_metrics_paths()
    stats_dir = paths["stats_dir"]
    copy_dir = os.path.join(os.path.dirname(stats_dir), "copy_paste_solution")

    return {
        "stats_dir_exists": str(os.path.exists(stats_dir)),
        "metrics_db_exists": str(os.path.exists(paths["db_path"])),
        "excel_exists": str(os.path.exists(paths["excel_path"])),
        "copy_folder_exists": str(os.path.exists(copy_dir)),
        "metrics_db_path": paths["db_path"],
        "excel_path": paths["excel_path"],
    }


def _fetch_run_stats_from_db(db_path: str) -> Dict[str, Any]:
    defaults: Dict[str, Any] = {
        "total_runs": 0,
        "runs_today": 0,
        "avg_tokens_used": 0.0,
        "last_run_time": "",
    }

    if not os.path.exists(db_path):
        return defaults

    try:
        conn = sqlite3.connect(db_path)
        try:
            table_exists = conn.execute(
                "SELECT 1 FROM sqlite_master WHERE type='table' AND name='llm_runs'"
            ).fetchone()
            if not table_exists:
                return defaults

            row = conn.execute(
                """
                SELECT
                    COUNT(*) AS total_runs,
                    SUM(CASE WHEN date(timestamp) = date('now', 'localtime') THEN 1 ELSE 0 END) AS runs_today,
                    AVG(total_tokens) AS avg_tokens_used,
                    MAX(timestamp) AS last_run_time
                FROM llm_runs
                """
            ).fetchone()
        finally:
            conn.close()

        if row is None:
            return defaults

        total_runs = int(row[0] or 0)
        runs_today = int(row[1] or 0)
        avg_tokens_used = round(float(row[2] or 0.0), 2)
        last_run_time = str(row[3] or "")

        return {
            "total_runs": total_runs,
            "runs_today": runs_today,
            "avg_tokens_used": avg_tokens_used,
            "last_run_time": last_run_time,
        }
    except (sqlite3.Error, ValueError, TypeError):
        return defaults


def _fetch_run_stats_from_excel(excel_path: str) -> Dict[str, Any]:
    defaults: Dict[str, Any] = {
        "total_runs": 0,
        "runs_today": 0,
        "avg_tokens_used": 0.0,
        "last_run_time": "",
    }

    if not os.path.exists(excel_path):
        return defaults

    try:
        import pandas as pd

        usage_df = pd.read_excel(excel_path, sheet_name="Usage")
        if usage_df.empty:
            return defaults

        total_runs = int(len(usage_df.index))
        runs_today = 0
        avg_tokens_used = 0.0
        last_run_time = ""

        if "timestamp" in usage_df.columns:
            timestamps = pd.to_datetime(usage_df["timestamp"], errors="coerce")
            valid_timestamps = timestamps.dropna()
            if not valid_timestamps.empty:
                today = pd.Timestamp.now().normalize()
                runs_today = int((valid_timestamps.dt.normalize() == today).sum())
                last_run_time = valid_timestamps.max().strftime("%Y-%m-%d %H:%M:%S")

        if "total_tokens" in usage_df.columns:
            total_tokens_series = pd.to_numeric(usage_df["total_tokens"], errors="coerce").dropna()
            if not total_tokens_series.empty:
                avg_tokens_used = round(float(total_tokens_series.mean()), 2)

        return {
            "total_runs": total_runs,
            "runs_today": runs_today,
            "avg_tokens_used": avg_tokens_used,
            "last_run_time": last_run_time,
        }
    except Exception:
        return defaults


def get_status() -> Dict[str, Any]:
    """Return a lightweight JSON-safe status snapshot for external orchestration."""
    paths = get_metrics_paths()
    db_path = paths["db_path"]
    excel_path = paths["excel_path"]

    try:
        tags_response = requests.get("http://localhost:11434/api/tags", timeout=3)
        ollama_reachable = tags_response.status_code == 200
    except requests.RequestException:
        ollama_reachable = False

    runs = _fetch_run_stats_from_db(db_path)
    if runs["total_runs"] == 0:
        excel_runs = _fetch_run_stats_from_excel(excel_path)
        if excel_runs["total_runs"] > 0:
            runs = excel_runs

    return {
        "system": {
            "ollama_reachable": ollama_reachable,
            "database_exists": os.path.exists(db_path),
        },
        "runs": {
            "total_runs": int(runs["total_runs"]),
            "runs_today": int(runs["runs_today"]),
            "avg_tokens_used": float(runs["avg_tokens_used"]),
            "last_run_time": str(runs["last_run_time"]),
        },
        "prompt": {
            "current_prompt_version": PROMPT_VERSION,
        },
    }
