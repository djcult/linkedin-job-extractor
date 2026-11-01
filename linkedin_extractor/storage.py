"""Store captures in JSON and readable Markdown."""
import json
from pathlib import Path


def save_job(job, directory: Path):
    directory.mkdir(parents=True, exist_ok=True)
    stem = job["job_id"]
    json_path = directory / f"{stem}.json"
    markdown_path = directory / f"{stem}.md"
    json_path.write_text(json.dumps(job, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    markdown = (
        f"# {job['title'] or 'Untitled job'}\n\n"
        f"**Company:** {job['company']}\n\n"
        f"**Location:** {job['location']}\n\n"
        f"**Source:** {job['url']}\n\n"
        f"**Captured:** {job['captured_at']}\n\n"
        f"## Description\n\n{job['description']}\n"
    )
    markdown_path.write_text(markdown, encoding="utf-8")
    return json_path, markdown_path
