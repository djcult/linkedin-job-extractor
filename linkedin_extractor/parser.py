"""Best-effort extraction from the currently displayed LinkedIn page."""
import re
from datetime import datetime, timezone
from urllib.parse import urlparse

SELECTORS = {
    "title": ["h1.top-card-layout__title", "h1.job-details-jobs-unified-top-card__job-title", "h1"],
    "company": [".topcard__org-name-link", ".top-card-layout__card a.topcard__org-name-link", ".job-details-jobs-unified-top-card__company-name", ".topcard__flavor"],
    "location": [".topcard__flavor--bullet", ".job-details-jobs-unified-top-card__bullet", ".top-card-layout__first-subline"],
    "description": [".jobs-description__content", ".jobs-box__html-content", ".show-more-less-html__markup", ".description__text", "#job-details"],
}


def job_id_from_url(url):
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https") or parsed.hostname not in ("linkedin.com", "www.linkedin.com"):
        raise ValueError(f"Not a LinkedIn URL: {url}")
    match = re.search(r"/jobs/view/(\\d+)(?:/|$)", parsed.path)
    if not match:
        raise ValueError(f"Expected LinkedIn /jobs/view/<id>/ URL: {url}")
    return match.group(1)


def first_text(page, selectors):
    for selector in selectors:
        locator = page.locator(selector)
        if locator.count():
            text = locator.first.inner_text(timeout=3000).strip()
            if text:
                return text
    return ""


def parse_job(page, url):
    title = first_text(page, SELECTORS["title"])
    description = first_text(page, SELECTORS["description"])
    company = first_text(page, SELECTORS["company"])
    location = first_text(page, SELECTORS["location"])
    return {
        "job_id": job_id_from_url(url),
        "url": url,
        "title": title,
        "company": company,
        "location": location,
        "description": description,
        "captured_at": datetime.now(timezone.utc).isoformat(),
    }
