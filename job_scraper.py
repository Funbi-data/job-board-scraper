"""
Job Board Scraper - Jobs to Submit on Sunday
--------------------------------------------
This script scrapes remote AI/Data/ML jobs from multiple job boards
and saves them into a CSV file.

Boards Included:
- RemoteOK
- WeWorkRemotely
- Indeed (basic example)
- Lever job pages (optional)

Requirements:
pip install requests beautifulsoup4 pandas lxml

Run:
python job_scraper.py
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0 Safari/537.36"
    )
}

jobs = []


# =========================================================
# REMOTEOK SCRAPER
# =========================================================
def scrape_remoteok():
    print("Scraping RemoteOK...")

    url = "https://remoteok.com/remote-python-jobs"

    response = requests.get(url, headers=HEADERS)

    soup = BeautifulSoup(response.text, "lxml")

    rows = soup.find_all("tr", class_="job")

    for row in rows:
        try:
            title = row.find("h2").text.strip()
            company = row.find("h3").text.strip()

            link_tag = row.find("a", itemprop="url")
            link = "https://remoteok.com" + link_tag["href"]

            jobs.append({
                "source": "RemoteOK",
                "title": title,
                "company": company,
                "link": link,
                "date_scraped": datetime.now().strftime("%Y-%m-%d")
            })

        except Exception:
            continue


# =========================================================
# WE WORK REMOTELY SCRAPER
# =========================================================
def scrape_weworkremotely():
    print("Scraping WeWorkRemotely...")

    url = "https://weworkremotely.com/remote-jobs/search?term=python"

    response = requests.get(url, headers=HEADERS)

    soup = BeautifulSoup(response.text, "lxml")

    sections = soup.find_all("li")

    for job in sections:
        try:
            company = job.find("span", class_="company").text.strip()
            title = job.find("span", class_="title").text.strip()

            link = "https://weworkremotely.com" + job.find("a")["href"]

            jobs.append({
                "source": "WeWorkRemotely",
                "title": title,
                "company": company,
                "link": link,
                "date_scraped": datetime.now().strftime("%Y-%m-%d")
            })

        except Exception:
            continue


# =========================================================
# INDEED SCRAPER
# =========================================================
def scrape_indeed():
    print("Scraping Indeed...")

    url = (
        "https://www.indeed.com/jobs?"
        "q=python+developer&l=Remote"
    )

    response = requests.get(url, headers=HEADERS)

    soup = BeautifulSoup(response.text, "lxml")

    cards = soup.find_all("div", class_="job_seen_beacon")

    for card in cards:
        try:
            title = card.find("h2").text.strip()
            company = card.find("span", class_="companyName").text.strip()

            link_tag = card.find("a")
            link = "https://www.indeed.com" + link_tag["href"]

            jobs.append({
                "source": "Indeed",
                "title": title,
                "company": company,
                "link": link,
                "date_scraped": datetime.now().strftime("%Y-%m-%d")
            })

        except Exception:
            continue


# =========================================================
# FILTER SUNDAY SUBMISSION JOBS
# =========================================================
def filter_jobs():
    """
    Example filter:
    Keep only AI/Data/Python related jobs
    """

    keywords = [
        "python",
        "ai",
        "machine learning",
        "data",
        "ml engineer",
        "backend",
        "automation",
    ]

    filtered = []

    for job in jobs:
        title = job["title"].lower()

        if any(keyword in title for keyword in keywords):
            filtered.append(job)

    return filtered


# =========================================================
# SAVE TO CSV
# =========================================================
def save_to_csv(filtered_jobs):
    df = pd.DataFrame(filtered_jobs)

    filename = (
        f"sunday_job_submissions_"
        f"{datetime.now().strftime('%Y%m%d')}.csv"
    )

    df.to_csv(filename, index=False)

    print(f"\nSaved {len(df)} jobs to {filename}")


# =========================================================
# MAIN
# =========================================================
if __name__ == "__main__":

    scrape_remoteok()
    scrape_weworkremotely()
    scrape_indeed()

    filtered_jobs = filter_jobs()

    save_to_csv(filtered_jobs)

    print("\nDone scraping jobs.")
