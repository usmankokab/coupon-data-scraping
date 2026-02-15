#!/usr/bin/env python
"""
╔════════════════════════════════════════════════════════════════╗
║         TRAVELOKA COUPON SCRAPER (PRODUCTION)                  ║
║  Extract coupons & offers from Cuponation Singapore website    ║
║  With advanced anti-bot measures & reliable extraction         ║
╚════════════════════════════════════════════════════════════════╝
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import time
import random
from datetime import datetime
from pathlib import Path
import sys


class TravelokaScraper:
    """
    Professional Traveloka coupon and deals scraper
    - Mimics real user behavior to avoid bot detection
    - Extracts coupons with codes & expiry dates
    - Extracts offers/deals with discounts
    """
    
    def __init__(self):
        self.user_agent_list = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        ]
        self.session = requests.Session()
        self.setup_session()
        self.coupons = []
        self.offers = []
        
    def setup_session(self):
        """Configure session to mimic real browser"""
        headers = {
            'User-Agent': random.choice(self.user_agent_list),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
            'Referer': 'https://www.google.com/',
        }
        self.session.headers.update(headers)
        self.session.timeout = 15
        
    def fetch_page(self, url):
        """Fetch webpage with human-like delays"""
        try:
            # Random delay to appear human-like
            delay = random.uniform(1, 3)
            print(f"📥 Fetching: {url}")
            print(f"   (Waiting {delay:.1f}s to appear human-like)")
            time.sleep(delay)
            
            response = self.session.get(url, allow_redirects=True, verify=True)
            response.raise_for_status()
            
            print(f"✅ Response: {response.status_code}")
            print(f"   Size: {len(response.content):,} bytes")
            return response.text
            
        except requests.exceptions.Timeout:
            print("❌ Connection timeout - server took too long")
            return None
        except requests.exceptions.ConnectionError:
            print("❌ Connection failed - check internet")
            return None
        except requests.exceptions.HTTPError as e:
            print(f"❌ HTTP Error: {e.response.status_code}")
            return None
        except Exception as e:
            print(f"❌ Error: {str(e)[:100]}")
            return None
    
    def parse_items(self, html):
        """Extract coupons and offers from HTML"""
        soup = BeautifulSoup(html, 'html.parser')
        h3_tags = soup.find_all('h3')
        
        print(f"\n🔍 Extracting data from {len(h3_tags)} items...")
        
        for h3 in h3_tags:
            try:
                description = h3.get_text(strip=True)
                if not description or len(description) < 10:
                    continue
                
                # Find parent container with complete info
                parent = h3
                full_text = description
                
                for _ in range(10):
                    parent = parent.find_parent()
                    if not parent:
                        break
                    parent_text = parent.get_text()
                    if re.search(r'\d{1,2}/\d{1,2}/\d{4}', parent_text):
                        full_text = parent_text
                        break
                
                # Extract discount code
                code = self._extract_code(description, full_text)
                
                # Extract expiry date
                date_match = re.search(r'(\d{1,2}/\d{1,2}/\d{4})', full_text)
                expiry = date_match.group(1) if date_match else 'N/A'
                
                # Classify and store
                if code != 'N/A' and expiry != 'N/A':
                    self.coupons.append({
                        'type': 'coupon',
                        'description': description,
                        'code': code,
                        'expiry_date': expiry,
                        'scraped_at': datetime.now().isoformat()
                    })
                elif code != 'N/A':
                    self.offers.append({
                        'type': 'offer',
                        'description': description,
                        'discount': code,
                        'scraped_at': datetime.now().isoformat()
                    })
                    
            except Exception:
                pass
        
        self._remove_duplicates()
    
    def _extract_code(self, description, full_text):
        """Extract discount code from text"""
        combined = f"{description} {full_text}"
        
        # Check for percentage
        pct = re.search(r'(\d+)%\s*(?:OFF|off|savings)', combined)
        if pct:
            return f"{pct.group(1)}%OFF"
        
        # Check for dollar amount
        dollar = re.search(r'\$(\d+)\s*(?:OFF|off|savings)', combined)
        if dollar:
            return f"${dollar.group(1)}OFF"
        
        # Check for credits
        if 'CREDITS' in combined:
            credits = re.search(r'\$(\d+)\s*CREDITS', combined)
            return f"${credits.group(1)}CREDITS" if credits else '$8CREDITS'
        
        # Check for gift card
        if 'GIFTCARD' in combined or 'GIFT CARD' in combined:
            return 'GIFTCARD'
        
        return 'N/A'
    
    def _remove_duplicates(self):
        """Remove duplicate entries"""
        seen = set()
        unique_coupons = []
        for c in self.coupons:
            key = (c['description'], c['code'], c['expiry_date'])
            if key not in seen:
                seen.add(key)
                unique_coupons.append(c)
        self.coupons = unique_coupons
        
        seen = set()
        unique_offers = []
        for o in self.offers:
            key = (o['description'], o['discount'])
            if key not in seen:
                seen.add(key)
                unique_offers.append(o)
        self.offers = unique_offers
    
    def _save_as_txt(self, output_dir):
        """Save results as human-readable text file"""
        txt_file = output_dir / 'traveloka_coupons.txt'
        
        with open(txt_file, 'w', encoding='utf-8') as f:
            # Header
            f.write('='*80 + '\n')
            f.write('TRAVELOKA COUPONS & OFFERS REPORT\n')
            f.write('='*80 + '\n\n')
            
            # Metadata
            f.write(f'Scraped on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
            f.write(f'Source: https://www.cuponation.com.sg/traveloka-promo-code\n')
            f.write(f'Total Coupons: {len(self.coupons)}\n')
            f.write(f'Total Offers: {len(self.offers)}\n')
            f.write(f'Total Items: {len(self.coupons) + len(self.offers)}\n')
            f.write('\n' + '='*80 + '\n\n')
            
            # Coupons Section
            f.write('COUPONS\n')
            f.write('-'*80 + '\n\n')
            
            for i, coupon in enumerate(self.coupons, 1):
                f.write(f'{i}. {coupon["description"]}\n')
                f.write(f'   Code: {coupon["code"]}\n')
                f.write(f'   Expires: {coupon["expiry_date"]}\n')
                f.write(f'   Scraped: {coupon["scraped_at"]}\n')
                f.write('\n')
            
            # Offers Section
            f.write('\n' + '='*80 + '\n')
            f.write('OFFERS & DEALS\n')
            f.write('-'*80 + '\n\n')
            
            if self.offers:
                for i, offer in enumerate(self.offers, 1):
                    f.write(f'{i}. {offer["description"]}\n')
                    f.write(f'   Discount: {offer["discount"]}\n')
                    f.write(f'   Scraped: {offer["scraped_at"]}\n')
                    f.write('\n')
            else:
                f.write('No offers found in this run.\n\n')
            
            # Footer
            f.write('\n' + '='*80 + '\n')
            f.write('END OF REPORT\n')
            f.write('='*80 + '\n')
        
        print(f"   ✅ output/traveloka_coupons.txt")
    
    def save_results(self):
        """Save to JSON, CSV, and TXT formats"""
        output = Path('output')
        output.mkdir(exist_ok=True)
        
        print(f"\n💾 Saving {len(self.coupons) + len(self.offers)} items...")
        
        # JSON files
        with open(output / 'coupons.json', 'w', encoding='utf-8') as f:
            json.dump(self.coupons, f, indent=2, ensure_ascii=False)
        print(f"   ✅ output/coupons.json ({len(self.coupons)} items)")
        
        with open(output / 'offers.json', 'w', encoding='utf-8') as f:
            json.dump(self.offers, f, indent=2, ensure_ascii=False)
        print(f"   ✅ output/offers.json ({len(self.offers)} items)")
        
        with open(output / 'all_results.json', 'w', encoding='utf-8') as f:
            json.dump({
                'scraped_at': datetime.now().isoformat(),
                'source': 'https://www.cuponation.com.sg/traveloka-promo-code',
                'summary': {
                    'total_coupons': len(self.coupons),
                    'total_offers': len(self.offers),
                    'total_items': len(self.coupons) + len(self.offers)
                },
                'coupons': self.coupons,
                'offers': self.offers
            }, f, indent=2, ensure_ascii=False)
        print(f"   ✅ output/all_results.json")
        
        # CSV for spreadsheets
        with open(output / 'coupons.csv', 'w', encoding='utf-8') as f:
            f.write('TYPE,DESCRIPTION,CODE_OR_DISCOUNT,EXPIRY_DATE,SCRAPED_AT\n')
            for c in self.coupons:
                desc = c['description'].replace('"', '""')
                f.write(f'coupon,"{desc}","{c["code"]}","{c["expiry_date"]}","{c["scraped_at"]}"\n')
            for o in self.offers:
                desc = o['description'].replace('"', '""')
                f.write(f'offer,"{desc}","{o["discount"]}","","{o["scraped_at"]}"\n')
        print(f"   ✅ output/coupons.csv")
        
        # Save as TXT (human-readable format)
        self._save_as_txt(output)
    
    def run(self):
        """Execute the scraper"""
        url = 'https://www.cuponation.com.sg/traveloka-promo-code'
        html = self.fetch_page(url)
        
        if not html:
            return False
        
        self.parse_items(html)
        
        if self.coupons or self.offers:
            self.save_results()
            return True
        
        print("⚠️  No data extracted")
        return False


def main():
    """Main entry point"""
    print("\n" + "="*70)
    print("🚀 TRAVELOKA COUPON SCRAPER")
    print("="*70)
    
    # Check dependencies
    try:
        import requests
        from bs4 import BeautifulSoup
    except ImportError:
        print("❌ Missing dependencies!")
        print("\nInstall with:")
        print("  pip install requests beautifulsoup4")
        return False
    
    print(f"\n⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n🔒 Anti-Bot Features:")
    print("   ✓ Rotating user agents")
    print("   ✓ Random request delays (1-3 seconds)")
    print("   ✓ Realistic HTTP headers")
    print("   ✓ Natural referer")
    print("   ✓ Connection pooling")
    
    scraper = TravelokaScraper()
    success = scraper.run()
    
    print("\n" + "="*70)
    if success:
        print("✅ SCRAPING SUCCESSFUL!")
        total = len(scraper.coupons) + len(scraper.offers)
        print(f"\n📊 Results:")
        print(f"   Coupons found: {len(scraper.coupons)}")
        print(f"   Offers found: {len(scraper.offers)}")
        print(f"   Total items: {total}")
        print(f"\n📁 Output files:")
        print(f"   • output/coupons.json")
        print(f"   • output/offers.json")
        print(f"   • output/all_results.json")
        print(f"   • output/coupons.csv (Excel/Sheets compatible)")
        print(f"   • output/traveloka_coupons.txt (Human-readable)")
        print("\n💡 Tip: Open coupons.csv in Excel or traveloka_coupons.txt in any text editor")
    else:
        print("❌ Scraping failed")
        return False
    
    print("="*70 + "\n")
    return True


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
