# first_linkedinScraper_app

A practical and simple LinkedIn scraping tool built using Python + Selenium + BeautifulSoup, designed to collect detailed information from public LinkedIn profiles, including names, headlines, experience, education, and even contact information, in a structured and reusable format.

This project was created as an experiment to automate the process of collecting structured professional data from LinkedIn profiles, especially those of top pre-seed venture capital (VC) investors.

By using this tool, I was able to successfully recover complete LinkedIn information of the top pre-seed VC investors in India, starting from a small list of just 20 public profile URLs.

## Project Overview

The idea behind first_linkedinScraper_app is straightforward, automate what humans usually do manually:

1. Visit a LinkedIn profile
2. Read the name, headline, and work experience
3. Open the "Contact Info" overlay to view email, phone, website, and birthday
4. Copy all this data into a spreadsheet

Doing that by hand for even 20–30 profiles can take hours. This scraper automates the entire flow, safely, reproducibly, and incrementally saving results so no data is lost if the session breaks midway.

Under the hood, it uses:

- **Selenium WebDriver** – to open and interact with LinkedIn pages
- **BeautifulSoup** – to parse and extract HTML data cleanly
- **Pandas** – to store and export results into a profiles.csv file
- **Fake User-Agent** – to simulate real browser behavior and avoid blocking
- **Pydantic** – for type-safe configuration and environment handling

## What It Can Do

Here's what the scraper extracts for every LinkedIn profile you provide:

| Field | Description |
|-------|-------------|
| **Name** | Full name of the person |
| **Headline** | The headline or title shown below their name |
| **LinkedIn_Id** | Their LinkedIn public ID |
| **Email** | All email addresses available under "Contact Info" |
| **Phone** | Any listed phone numbers |
| **Website** | Personal or company website links |
| **Birthday** | If visible on their contact page |
| **Experience** | List of positions, companies, dates, and descriptions |
| **Education** | Schools, degrees, and fields of study |

The output is stored as a single CSV file (`data/profiles.csv`), which can be easily imported into Excel, Google Sheets, or any data analysis tool.

## Project Structure

```
first_linkedinScraper_app/
│
├── config.py               # Environment variables and configuration
├── scraper.py              # Main scraper logic
├── utils.py                # Utility functions (driver init, login, save, etc.)
│
├── data/
│   ├── urls.txt            # List of LinkedIn profile URLs to scrape
│   ├── proxies.txt         # Optional proxy list
│   └── profiles.csv        # Output CSV after scraping
│
├── requirements.txt        # Python dependencies
├── .env.example            # Example environment configuration file
└── README.md               # This documentation
```

## Installation & Setup

This project is simple to run locally and doesn't require deep technical knowledge. Just follow these steps:

### 1. Clone the repository

```bash
git clone https://github.com/ihamdaan/aero-proj.git
cd first_linkedinScraper_app
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # for macOS/Linux
venv\Scripts\activate     # for Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

The `requirements.txt` file includes all necessary dependencies:
- selenium
- beautifulsoup4
- pandas
- fake-useragent
- pydantic
- pydantic-settings

### 4. Configure environment variables

An example file `.env.example` is included. Copy it and rename it to `.env` in the same folder.

```
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_password
```

**Tip:** If you don't want to use your personal LinkedIn account, you can use a temporary email from https://temp-mail.org/en/. That's what I used for repeated testing safely, it allowed me to log in multiple times and verify the scraper thoroughly.

### 5. Add profile URLs to data/urls.txt

Each line in this file should contain one LinkedIn profile URL. Example:

```
https://www.linkedin.com/in/janedoe/
https://www.linkedin.com/in/johndoe/
```

I've included 20 LinkedIn profiles of top pre-seed VC investors in the data/ folder so you can test immediately.

## Running the Scraper

Once everything is ready, just run:

```bash
python scraper.py
```

The script will:

1. Open Chrome (headless if configured)
2. Log in to LinkedIn using your credentials
3. Read profile URLs from data/urls.txt
4. Extract all data (including contact info overlay)
5. Save results incrementally into data/profiles.csv

Every time it completes a profile, it saves progress, so even if your internet drops or LinkedIn rate-limits you, you won't lose work.

## How It Works

- **config.py** – Reads credentials from .env securely using pydantic
- **utils.py** – Handles driver setup, LinkedIn login, random user-agents, proxies, and CSV saving
- **scraper.py** – The main workflow that loads profile URLs, visits each one, extracts visible sections (Name, Headline, Experience, Education), visits the contact-info endpoint to fetch hidden data, and saves everything incrementally

No extra API or complicated dependencies, just clean, browser-based scraping logic.

## Troubleshooting Tips

| Problem | Likely Cause | Fix |
|---------|--------------|-----|
| Login fails immediately | Wrong LinkedIn credentials or captcha | Try using a fresh temp email or non-headless mode |
| Scraper hangs on profile load | Slow connection or page not found | Increase WebDriverWait timeout |
| Empty contact info | Profile hides it or account not logged in | Double-check login session or try another profile |
| "chromedriver not found" | Missing driver setup | Update Chrome or reinstall Selenium |

## Ethical Use Disclaimer

This tool is built purely for educational and research purposes, to understand automated browser workflows, structured scraping, and LinkedIn's DOM behavior.

Do not use it for commercial data harvesting or spam. Always respect LinkedIn's robots.txt and user privacy policies.

## Conclusion

The first_linkedinScraper_app demonstrates how a simple, well-structured Python tool can automate a real-world task like LinkedIn data collection in a safe, efficient way.

It's easy to understand, easy to modify, and flexible enough to adapt for other professional scraping tasks, from talent discovery to competitive mapping.

With a single command, you can now extract structured, multi-field profile data from LinkedIn into a clean CSV file, a huge timesaver for any research or data analysis workflow.