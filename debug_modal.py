"""
Debug script to see what's on the voucher/modal page
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

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
    
    # Accept cookies
    try:
        driver.execute_script("""
            const btn = Array.from(document.querySelectorAll('button, a'))
                .find(el => el.textContent.includes('ACCEPT'));
            if (btn) btn.click();
        """)
        time.sleep(1)
    except:
        pass
    
    # Find first See Promo Code button
    btn = driver.find_element(By.XPATH, "//*[contains(text(), 'See promo code')][@role='button']")
    original_window = driver.current_window_handle
    
    # Scroll and click
    driver.execute_script("arguments[0].scrollIntoView(true);", btn)
    time.sleep(0.5)
    driver.execute_script("arguments[0].click();", btn)
    print("Clicked button")
    
    time.sleep(3)
    
    # Switch to new tab
    all_windows = driver.window_handles
    for window in all_windows:
        if window != original_window:
            driver.switch_to.window(window)
            break
    
    print(f"URL: {driver.current_url}")
    print(f"\n=== FULL PAGE TEXT ===")
    print(driver.execute_script("return document.body.innerText;"))
    
    print(f"\n=== H1, H2, H3 elements ===")
    for tag in ['h1', 'h2', 'h3']:
        elements = driver.find_elements(By.XPATH, f"//{tag}")
        for e in elements:
            print(f"{tag}: {e.text.strip()}")
    
    print(f"\n=== All elements with class containing 'title' or 'heading' ===")
    elements = driver.find_elements(By.XPATH, "//*[contains(@class, 'title') or contains(@class, 'heading') or contains(@class, 'promo')]")
    for e in elements[:10]:
        print(f"Class: {e.get_attribute('class')}, Text: {e.text.strip()[:100]}")
    
    print(f"\n=== Code elements ===")
    code_elements = driver.find_elements(By.XPATH, "//code | //*[contains(@class, 'code')] | //h4")
    for e in code_elements[:10]:
        print(f"Tag: {e.tag_name}, Text: {e.text.strip()}")
    
finally:
    driver.quit()
