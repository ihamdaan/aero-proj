# scraper.py
import os
import time
import random
import json
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import init_driver, login_linkedin, random_delay, save_to_csv

DATA_DIR = "data"
URL_FILE = os.path.join(DATA_DIR, "urls.txt")
OUTPUT_FILE = os.path.join(DATA_DIR, "profiles.csv")


def read_urls():
    """Read all profile URLs from data/urls.txt"""
    if not os.path.exists(URL_FILE):
        raise FileNotFoundError(f"[ERROR] Missing {URL_FILE}")
    with open(URL_FILE, "r") as f:
        urls = [line.strip() for line in f.readlines() if line.strip()]
    print(f"[INFO] Loaded {len(urls)} profile URLs.")
    return urls


def extract_contact_info(driver, url):
    """Scrape Name, Headline, Experience, Education, and Contact Info efficiently."""
    profile = {
        "VisitingSite_URL": url,
        "Name": "NA",
        "Headline": "NA",
        "LinkedIn_Id": "NA",
        "Email": "NA",
        "Phone": "NA",
        "Website": "NA",
        "Birthday": "NA",
        "Experience": "NA",
        "Education": "NA",
    }

    try:
        # ---------------- STEP 1: Open Profile Once ----------------
        driver.get(url)
        WebDriverWait(driver, 12).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1"))
        )
        time.sleep(1)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        # --- Name ---
        name_el = soup.select_one("h1")
        if name_el:
            profile["Name"] = name_el.get_text(strip=True)

        # --- Headline ---
        headline_el = soup.select_one("div.text-body-medium.break-words")
        if headline_el:
            profile["Headline"] = headline_el.get_text(strip=True)

        # ---------------- STEP 2: Extract Experience ----------------
        exp_section = soup.find("section", {"id": "experience"})
        experiences = []
        if exp_section:
            exp_items = exp_section.find_all("li", class_="artdeco-list__item")
            for item in exp_items:
                title = item.find("span", {"aria-hidden": "true"})
                company = item.find("span", class_="t-14 t-normal")
                dates = item.find("span", class_="pvs-entity__caption-wrapper")
                location = item.find("span", class_="t-14 t-normal t-black--light")
                desc = item.find("div", class_="inline-show-more-text")

                experiences.append({
                    "title": title.get_text(strip=True) if title else "NA",
                    "company": company.get_text(strip=True) if company else "NA",
                    "dates": dates.get_text(strip=True) if dates else "NA",
                    "location": location.get_text(strip=True) if location else "NA",
                    "description": desc.get_text(strip=True) if desc else "NA",
                })
        profile["Experience"] = json.dumps(experiences, ensure_ascii=False) if experiences else "NA"

        # ---------------- STEP 3: Extract Education ----------------
        edu_section = soup.find("section", {"id": "education"})
        educations = []
        if edu_section:
            edu_items = edu_section.find_all("li", class_="artdeco-list__item")
            for item in edu_items:
                school = item.find("span", {"aria-hidden": "true"})
                degree = item.find("span", class_="t-14 t-normal")
                field = item.find("span", class_="t-14 t-normal t-black")

                educations.append({
                    "school": school.get_text(strip=True) if school else "NA",
                    "degree": degree.get_text(strip=True) if degree else "NA",
                    "field": field.get_text(strip=True) if field else "NA",
                })
        profile["Education"] = json.dumps(educations, ensure_ascii=False) if educations else "NA"

        # ---------------- STEP 4: Visit Contact Info Overlay ----------------
        contact_url = url.rstrip("/") + "/overlay/contact-info/"
        driver.get(contact_url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "artdeco-modal__content"))
        )

        contact_soup = BeautifulSoup(driver.page_source, "html.parser")

        # LinkedIn URL
        linkedin_link = contact_soup.find("a", href=lambda x: x and "linkedin.com/in/" in x)
        if linkedin_link:
            profile["LinkedIn_Id"] = linkedin_link.get_text(strip=True)

        # Email(s)
        emails = [a.get_text(strip=True) for a in contact_soup.find_all("a", href=lambda x: x and x.startswith("mailto:"))]
        if emails:
            profile["Email"] = ", ".join(emails)

        # Phone(s)
        phone_section = contact_soup.find("h3", string=lambda x: x and "Phone" in x)
        if phone_section:
            phone_list = phone_section.find_next("ul")
            if phone_list:
                numbers = [
                    span.get_text(strip=True)
                    for span in phone_list.find_all("span", class_="t-14 t-black t-normal")
                ]
                profile["Phone"] = ", ".join(numbers)

        # Website(s)
        websites = [
            a["href"] for a in contact_soup.find_all("a", href=lambda x: x and "http" in x and "linkedin.com" not in x)
        ]
        if websites:
            profile["Website"] = ", ".join(websites)

        # Birthday
        bday = contact_soup.find("h3", string=lambda x: x and "Birthday" in x)
        if bday:
            date = bday.find_next("span", class_="t-14 t-black t-normal")
            if date:
                profile["Birthday"] = date.get_text(strip=True)

        print(f"[OK] Scraped: {profile['Name']}")

    except Exception as e:
        print(f"[WARN] Failed to scrape {url}: {e}")

    return profile


def main():
    driver = init_driver()
    login_linkedin(driver)

    urls = read_urls()
    results = []

    for idx, url in enumerate(urls, start=1):
        print(f"[{idx}/{len(urls)}] Scraping: {url}")
        data = extract_contact_info(driver, url)
        results.append(data)
        random_delay(2, 4)

        # 💾 Save progress incrementally
        save_to_csv(results, OUTPUT_FILE)
        print(f"[INFO] Progress saved after {idx} profiles.")

    driver.quit()
    print(f"[INFO] All done. Final results in {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
