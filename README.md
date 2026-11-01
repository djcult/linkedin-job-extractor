# LinkedIn Job Extractor

Local, manual-assisted LinkedIn job-description capture using Python and Playwright.

## Features
- Accept one or more LinkedIn job URLs.
- Launch a visible Chromium browser for each URL.
- You can sign in, expand **Show more**, and review the posting before capture.
- Extract title, company, location, description and other visible metadata where available.
- Write JSON and Markdown to `output/`.
- Avoid keeping passwords or browser profiles in the repository.

## Install (Windows PowerShell)

Requires Python 3.10+.

```powershell
git clone https://github.com/djcult/linkedin-job-extractor.git
cd linkedin-job-extractor
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m playwright install chromium
```

If your PowerShell policy disallows activation, use `.venv\Scripts\python.exe` instead of `python`.

## Run

```powershell
python extract.py https://www.linkedin.com/jobs/view/4478287225/
python extract.py https://www.linkedin.com/jobs/view/4476827452/ https://www.linkedin.com/jobs/view/4478287225/
```

A Chromium window opens. Navigate or sign in manually if required, expand the description, then return to the terminal and press Enter to save. Repeat for each URL. Results are in `output/<job-id>.json` and `output/<job-id>.md`.

## Notes
LinkedIn's markup and access restrictions change; fields are best-effort. Review extracted results. This utility does not attempt to evade CAPTCHA, rate limits or access controls. Use only for postings you are entitled to access, at low volume, consistent with applicable platform terms. Your output contains job text; it is ignored by Git.

## Tests

```powershell
python -m unittest discover -s tests
```
