"""Capture LinkedIn postings interactively in a visible browser."""
import argparse
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

from linkedin_extractor.parser import parse_job, job_id_from_url
from linkedin_extractor.storage import save_job


def main():
    parser = argparse.ArgumentParser(description="Manually assisted LinkedIn job capture")
    parser.add_argument("urls", nargs="+", help="LinkedIn jobs/view URLs")
    parser.add_argument("--output", default="output", help="Output directory")
    args = parser.parse_args()

    for url in args.urls:
        try:
            job_id_from_url(url)
        except ValueError as exc:
            parser.error(str(exc))

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        try:
            for url in args.urls:
                print(f"Opening {url}")
                try:
                    page.goto(url, wait_until="domcontentloaded", timeout=45000)
                except Exception as exc:
                    print(f"Navigation warning: {exc}")
                input("Review/expand the job in Chromium, then press Enter here to capture...")
                job = parse_job(page, url)
                if not job["description"]:
                    print("Warning: no description found. Check access and expand 'Show more'.")
                json_path, md_path = save_job(job, Path(args.output))
                print(f"Saved {json_path} and {md_path}")
        finally:
            browser.close()


if __name__ == "__main__":
    main()
