"""Debug script to see what happens when clicking GET DEAL"""

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
    url = "https://www.cuponation.com.sg/traveloka-promo-code"
    print(f"Loading {url}...")
    driver.get(url)
    time.sleep(5)
    
    # Find GET DEAL buttons
    offer_buttons = driver.find_elements(By.XPATH,
        "//div[@title='Get deal'][@role='button']"
    )
    print(f"Found {len(offer_buttons)} GET DEAL buttons")
    
    if offer_buttons:
        btn = offer_buttons[0]
        
        # Get title
        parent = btn
        for _ in range(10):
            parent_class = parent.get_attribute('class') or ""
            if '_6tavkoa' in parent_class:
                break
            try:
                parent = parent.find_element(By.XPATH, './..')
            except:
                break
        
        title_elems = parent.find_elements(By.XPATH, ".//h3 | .//h4")
        if title_elems:
            print(f"Title: {title_elems[0].text[:80]}")
        
        # Click the button
        print("Clicking GET DEAL button...")
        driver.execute_script("arguments[0].click();", btn)
        time.sleep(3)
        
        # Switch to new tab
        original_window = driver.current_window_handle
        all_windows = driver.window_handles
        new_window = None
        for window in all_windows:
            if window != original_window:
                new_window = window
                break
        
        if new_window:
            driver.switch_to.window(new_window)
            print(f"Switched to new tab")
            time.sleep(2)
            
            # Get page URL
            print(f"Page URL: {driver.current_url}")
            
            # Get page title
            print(f"Page title: {driver.title}")
            
            # Get all text
            body_text = driver.execute_script("return document.body.innerText;")
            print(f"\nPage text:\n{body_text[:2000]}")
            
            # Look for links
            links = driver.find_elements(By.XPATH, "//a[@href]")
            print(f"\nFound {len(links)} links")
            for i, l in enumerate(links[:10]):
                href = l.get_attribute('href')
                text = l.text[:50]
                print(f"  {i+1}. {text} -> {href}")
            
            # Look for GO TO STORE
            goto = driver.find_elements(By.XPATH, 
                "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'go to store')]"
            )
            print(f"\nFound {len(goto)} 'GO TO STORE' elements")
            for g in goto:
                print(f"  Tag: {g.tag_name}, Text: {g.text}")
                print(f"  Href: {g.get_attribute('href')}")
                print(f"  Onclick: {g.get_attribute('onclick')}")
        
finally:
    driver.quit()
