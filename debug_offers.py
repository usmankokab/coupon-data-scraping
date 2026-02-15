"""Debug script to find GET DEAL links"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920,1080')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    # Load the page
    url = "https://www.cuponation.com.sg/traveloka-promo-code"
    print(f"Loading {url}...")
    driver.get(url)
    time.sleep(5)
    
    # Get all text to see what's on page
    body_text = driver.execute_script("return document.body.innerText;")
    
    # Count different button types
    see_promo = driver.find_elements(By.XPATH, "//*[contains(text(), 'See promo code')]")
    get_deal = driver.find_elements(By.XPATH, "//*[contains(text(), 'GET DEAL')]")
    get_code = driver.find_elements(By.XPATH, "//*[contains(text(), 'GET CODE')]")
    
    print(f"\nSee promo code buttons: {len(see_promo)}")
    print(f"GET DEAL buttons: {len(get_deal)}")
    print(f"GET CODE buttons: {len(get_code)}")
    
    # Check for any link or button elements
    all_buttons = driver.find_elements(By.XPATH, "//button | //a")
    print(f"\nTotal buttons/links: {len(all_buttons)}")
    
    # Print sample of each type
    if get_deal:
        print("\n=== GET DEAL elements found ===")
        for i, el in enumerate(get_deal[:5]):
            print(f"{i+1}. Tag: {el.tag_name}, Text: {el.text[:50]}")
            try:
                print(f"   Class: {el.get_attribute('class')}")
                print(f"   Href: {el.get_attribute('href')}")
            except:
                pass
    
    # Check if there's a "Show All" or similar for offers
    show_all = driver.find_elements(By.XPATH, "//*[contains(text(), 'Show')]")
    print(f"\n'Show' elements: {len(show_all)}")
    
    # Try to find any deals/offers section
    deals = driver.find_elements(By.XPATH, "//*[contains(text(), 'deal')]")
    print(f"\n'deal' text elements: {len(deals)}")
    
    # Print a sample of what text is on the page
    print("\n=== Sample page text (first 2000 chars) ===")
    print(body_text[:2000])
    
finally:
    driver.quit()
