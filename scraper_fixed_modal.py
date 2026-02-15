"""
Traveloka Coupon Scraper - FIXED
Gets expiry from same card as See Promo Code button
Runs in headless mode
Also extracts OFFERS (GET DEAL links) - no code needed
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import time
import json
import csv
import re
import pyperclip
from datetime import datetime
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class TravelokaCodeScraper:
    def __init__(self):
        self.coupons = []
        self.offers = []
        self.driver = None
        
    def setup_driver(self):
        """Setup Chrome driver - headless mode"""
        try:
            options = Options()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-popup-blocking')
            # options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=1920,1080')
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            #print("[OK] Driver ready (headless mode)")
            return True
        except Exception as e:
            print(f"[ERROR] Driver setup failed: {e}")
            return False
    
    def run(self):
        """Main execution"""
        try:
            if not self.setup_driver():
                return False
            
            url = "https://www.cuponation.com.sg/traveloka-promo-code"
            print(f"Loading {url}...")
            self.driver.get(url)
            
            print("Waiting for page to load...")
            time.sleep(5)
            
            # Accept cookies
            try:
                self.driver.execute_script("""
                    const btn = Array.from(document.querySelectorAll('button, a'))
                        .find(el => el.textContent.includes('ACCEPT'));
                    if (btn) btn.click();
                """)
                time.sleep(1)
            except:
                pass
            
            print("Page loaded")
            
            # ===== Extract OFFERS (GET DEAL) first =====
            print("\n=== Extracting OFFERS (GET DEAL) ===")
            
            # Simply find GET DEAL buttons and get titles from main page (no clicking)
            offer_buttons = self.driver.find_elements(By.XPATH,
                "//div[@title='Get deal'][@role='button'] | //div[contains(@title, 'Get deal')][@role='button']"
            )
            print(f"Found {len(offer_buttons)} GET DEAL buttons")
            
            for i, btn in enumerate(offer_buttons):
                try:
                    # Get title from parent card
                    title = "N/A"
                    try:
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
                            title_text = title_elems[0].text.strip()
                            if len(title_text) > 10 and 'CODE' not in title_text.upper():
                                title = title_text[:200]
                    except:
                        pass
                    
                    if title != "N/A":
                        self.offers.append({
                            'title': title
                        })
                        print(f"  {i+1}. {title[:60]}")
                        
                except Exception as e:
                    print(f"  {i+1}. [ERROR] {str(e)[:40]}")
            
            print(f"Extracted {len(self.offers)} offers\n")
            
            # ===== Now extract COUPONS (SEE PROMO CODE) =====
            print("=== Extracting COUPONS (SEE PROMO CODE) ===")
            
            # Scroll to load all coupons
            print("Scrolling to load all coupons...")
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            
            for scroll_attempt in range(5):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                try:
                    load_more = self.driver.find_element(By.XPATH, 
                        "//button[contains(text(), 'Load More')] | //a[contains(text(), 'Load More')]"
                    )
                    self.driver.execute_script("arguments[0].click();", load_more)
                    time.sleep(2)
                except:
                    pass
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
            
            # Get all See Promo Code buttons
            promo_buttons = self.driver.find_elements(By.XPATH, 
                "//*[contains(text(), 'See promo code')][@role='button']"
            )
            max_coupons = len(promo_buttons)
            print(f"Found {max_coupons} coupons")
            
            # Get page text for titles
            body_text = self.driver.execute_script("return document.body.innerText;")
            sections = body_text.split("SEE PROMO CODE")
            
            original_window = self.driver.current_window_handle
            
            coupon_num = 0
            
            while coupon_num < max_coupons:
                try:
                    # Get fresh button
                    promo_buttons = self.driver.find_elements(By.XPATH, 
                        "//*[contains(text(), 'See promo code')][@role='button']"
                    )
                    
                    if coupon_num >= len(promo_buttons):
                        break
                    
                    btn = promo_buttons[coupon_num]
                    
                    # ===== Get title and expiry from the SAME CARD as the button =====
                    title = "N/A"
                    expiry = "N/A"
                    
                    try:
                        # Find parent card element - look for class containing '_6tavkoa'
                        parent = btn
                        for _ in range(10):  # Go up max 10 levels
                            parent_class = parent.get_attribute('class') or ""
                            if '_6tavkoa' in parent_class:
                                break
                            try:
                                parent = parent.find_element(By.XPATH, './..')
                            except:
                                break
                        
                        # Now look for expiry within this card
                        expiry_elems = parent.find_elements(By.XPATH, 
                            ".//span[contains(@class, 'az57m4c')] | .//span[contains(text(), 'Expiry')]"
                        )
                        if expiry_elems:
                            expiry_text = expiry_elems[0].text.strip()
                            match = re.search(r'(\d{1,2}/\d{1,2}/\d{4})', expiry_text)
                            if match:
                                expiry = match.group(1)
                                print(f"  Found expiry in card: {expiry}")
                        
                        # Also try to find title in the card
                        title_elems = parent.find_elements(By.XPATH, ".//h3 | .//h4")
                        if title_elems:
                            title_text = title_elems[0].text.strip()
                            if len(title_text) > 10 and 'CODE' not in title_text.upper():
                                title = title_text[:140]
                    
                    except Exception as e:
                        print(f"  Could not find in card: {str(e)[:40]}")
                    
                    # Fallback: get from page sections
                    if title == "N/A" or expiry == "N/A":
                        if coupon_num + 1 < len(sections):
                            section = sections[coupon_num + 1]
                            lines = [l.strip() for l in section.split('\n') if l.strip()]
                            for line in lines:
                                if expiry == "N/A":
                                    match = re.search(r'(\d{1,2}/\d{1,2}/\d{4})', line)
                                    if match:
                                        expiry = match.group(1)
                                if title == "N/A":
                                    if re.match(r'^Expiry:', line):
                                        continue
                                    if re.match(r'^\d+%?\s*OFF', line):
                                        continue
                                    if 'Verified' in line or 'arrow' in line or 'SEE PROMO' in line:
                                        continue
                                    if len(line) > 20:
                                        title = line[:140]
                                        break
                    
                    # ===== Click button and get code =====
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", btn)
                    time.sleep(0.5)
                    self.driver.execute_script("arguments[0].click();", btn)
                    print(f"  Clicked button {coupon_num+1}")
                    
                    time.sleep(3)
                    
                    # Switch to new tab
                    all_windows = self.driver.window_handles
                    new_window = None
                    for window in all_windows:
                        if window != original_window:
                            new_window = window
                            break
                    
                    if new_window:
                        self.driver.switch_to.window(new_window)
                    
                    time.sleep(2)
                    
                    # Get code from modal
                    actual_code = None
                    
                    # Try COPY button
                    copy_buttons = self.driver.find_elements(By.XPATH,
                        "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'copy')]"
                    )
                    
                    if copy_buttons:
                        pyperclip.copy("")
                        time.sleep(0.2)
                        self.driver.execute_script("arguments[0].click();", copy_buttons[0])
                        time.sleep(0.5)
                        actual_code = pyperclip.paste().strip()
                    
                    # Fallback: look in h4
                    if not actual_code or len(actual_code) < 2:
                        h4_elements = self.driver.find_elements(By.XPATH, "//h4")
                        for h4 in h4_elements:
                            text = h4.text.strip()
                            if text and 3 <= len(text) <= 20 and re.match(r'^[A-Za-z0-9]+$', text):
                                actual_code = text
                                break
                    
                    print(f"  Title: {title[:40] if title != 'N/A' else 'N/A'}")
                    print(f"  Code: {actual_code}")
                    print(f"  Expiry: {expiry}")
                    
                    # Close and go back
                    if new_window:
                        self.driver.close()
                        self.driver.switch_to.window(original_window)
                    
                    self.driver.get(url)
                    time.sleep(3)
                    
                    if actual_code and len(actual_code) > 1:
                        self.coupons.append({
                            'description': title,
                            'code': actual_code,
                            'expiry': expiry
                        })
                        print(f"{coupon_num+1:2d}. {actual_code:15s} | {title[:40] if title != 'N/A' else 'N/A'} | {expiry}")
                    
                    coupon_num += 1
                    
                except Exception as e:
                    print(f"{coupon_num+1:2d}. [ERROR] {str(e)[:60]}")
                    try:
                        if len(self.driver.window_handles) > 1:
                            for w in self.driver.window_handles:
                                if w != original_window:
                                    self.driver.switch_to.window(w)
                                    self.driver.close()
                        self.driver.switch_to.window(original_window)
                        self.driver.get(url)
                        time.sleep(2)
                    except:
                        pass
                    coupon_num += 1
                    continue
            
            print(f"\nExtracted {len(self.coupons)} coupons")
            
            if self.coupons:
                self.save()
            
            return len(self.coupons) > 0
            
        except Exception as e:
            print(f"[ERROR] {e}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            if self.driver:
                self.driver.quit()
                print("Browser closed")
    
    def save(self):
        """Save results"""
        p = Path('output')
        p.mkdir(exist_ok=True)
        
        print(f"Saving to output/...")
        
        # Save COUPONS
        simplified_coupons = []
        for c in self.coupons:
            title = c.get('description', 'N/A')
            if title == 'N/A':
                title = c.get('code', 'N/A')
            simplified_coupons.append({
                'Title': title,
                'Code': c.get('code', 'N/A'),
                'Expires': c.get('expiry', 'N/A')
            })
        
        (p / 'coupons.json').write_text(json.dumps(simplified_coupons, ensure_ascii=False, indent=2), encoding='utf-8')
        print("   coupons.json")
        
        with open(p / 'coupons.csv', 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['Title', 'Code', 'Expires'])
            writer.writeheader()
            writer.writerows(simplified_coupons)
        print("   coupons.csv")
        
        # Save OFFERS
        (p / 'offers.json').write_text(json.dumps(self.offers, ensure_ascii=False, indent=2), encoding='utf-8')
        print("   offers.json")
        
        with open(p / 'offers.csv', 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['title'])
            writer.writeheader()
            writer.writerows(self.offers)
        print("   offers.csv")
        
        # Save combined text report
        txt = "TRAVELOKA OFFERS (GET DEAL - No Code Required)\n"
        txt += "="*60 + "\n\n"
        
        for o in self.offers:
            txt += f"Title: {o.get('title', 'N/A')}\n\n"
        
        txt += "\n" + "="*60 + "\n"
        txt += "TRAVELOKA COUPONS (SEE PROMO CODE - Code Required)\n"
        txt += "="*60 + "\n\n"
        
        for c in simplified_coupons:
            txt += f"Title: {c['Title']}\n"
            txt += f"Code: {c['Code']}\n"
            txt += f"Expires: {c['Expires']}\n\n"
        
        txt += "="*60 + "\n"
        (p / 'traveloka_coupons.txt').write_text(txt, encoding='utf-8')
        print("   traveloka_coupons.txt")
        
        (p / 'all_results.json').write_text(json.dumps({
            'timestamp': datetime.now().isoformat(),
            'total_coupons': len(simplified_coupons),
            'total_offers': len(self.offers),
            'coupons': simplified_coupons,
            'offers': self.offers
        }, ensure_ascii=False, indent=2), encoding='utf-8')
        print("   all_results.json")
        
        print(f"\nTotal: {len(simplified_coupons)} coupons, {len(self.offers)} offers")
        print("All files saved!")


if __name__ == "__main__":
    TravelokaCodeScraper().run()
