# utils.py
import random
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from config import settings


def init_driver(use_proxy: bool = False) -> webdriver.Chrome:
    """Initialize Selenium Chrome driver with user-agent and optional proxy."""
    ua = UserAgent()
    options = Options()
    options.add_argument(f"user-agent={ua.random}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--log-level=3")
    if settings.headless:
        options.add_argument("--headless=new")

    if use_proxy:
        proxy = get_random_proxy()
        if proxy:
            options.add_argument(f"--proxy-server={proxy}")
            print(f"[INFO] Using proxy: {proxy}")

    # ✅ Selenium auto-manages the driver now
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    print("[INFO] ChromeDriver initialized successfully.")
    return driver


def get_random_proxy() -> str | None:
    """Fetch a random proxy from file if available."""
    try:
        with open(settings.proxy_list_path, "r") as f:
            proxies = [p.strip() for p in f.readlines() if p.strip()]
        return random.choice(proxies) if proxies else None
    except FileNotFoundError:
        return None


def login_linkedin(driver):
    """Perform LinkedIn login using credentials from .env."""
    print("[INFO] Logging into LinkedIn...")
    driver.get("https://www.linkedin.com/login")
    email_input = driver.find_element(By.ID, "username")
    password_input = driver.find_element(By.ID, "password")
    email_input.send_keys(settings.linkedin_email)
    password_input.send_keys(settings.linkedin_password)
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    time.sleep(5)
    print(f"[INFO] Logged in → Current URL: {driver.current_url}")


def random_delay(min_time=2, max_time=5):
    """Pause randomly between requests."""
    time.sleep(random.uniform(min_time, max_time))


def save_to_csv(data, path="data/profiles.csv"):
    """Save results to CSV."""
    df = pd.DataFrame(data)
    df.to_csv(path, index=False, encoding="utf-8")
    print(f"[INFO] Saved {len(data)} profiles → {path}")
