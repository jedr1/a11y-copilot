from playwright.sync_api import sync_playwright
import os

def take_webpage_screenshot(url, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with sync_playwright() as p:
       browser = p.chromium.launch()
       page = browser.new_page()
       page.goto(url)
       page.screenshot(path=file_path, full_page=True)
       browser.close()
    return file_path