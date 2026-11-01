"""Capture LinkedIn postings interactively in a visible browser."""
import argparse
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

    saved = skipped = 0
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        try:
            for index, url in enumerate(args.urls, start=1):
                print(f"\\n[{index}/{len(args.urls)}] Opening {url}")
                try:
                    page.goto(url, wait_until="domcontentloaded", timeout=45000)
                except Exception as exc:
                    print(f"Navigation warning: {exc}")

                while True:
                    choice = input(
                        "[Enter] save  |  [s] skip expired/unavailable  |  [q] quit: "
                    ).strip().lower()
                    if choice in ("", "s", "q"):
                        break
                    print("Please press Enter, s, or q.")

                if choice == "q":
                    print("Stopped by user.")
                    break
                if choice == "s":
                    skipped += 1
                    print("Skipped; no files saved.")
                    continue

                job = parse_job(page, url)
                if not job["description"]:
                    print("Warning: no description found. Check access and expand 'Show more'.")
                json_path, md_path = save_job(job, Path(args.output))
                saved += 1
                print(f"Saved {json_path} and {md_path}")
        finally:
            browser.close()
    print(f"Finished: {saved} saved, {skipped} skipped.")


if __name__ == "__main__":
    main()
