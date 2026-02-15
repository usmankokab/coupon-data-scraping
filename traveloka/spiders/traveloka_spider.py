import scrapy
import json
from datetime import datetime
import random
import time


class TravelokaCouponSpider(scrapy.Spider):
    """
    Spider to scrape Traveloka coupons and offers from Singapore
    Configured to mimic real user behavior and avoid bot detection
    """
    names = 'traveloka_coupon'
    allowed_domains = ['cuponation.com.sg']
    start_urls = ['https://www.cuponation.com.sg/traveloka-promo-code']
    
    def __init__(self, *args, **kwargs):
        super(TravelokaCouponSpider, self).__init__(*args, **kwargs)
        self.coupons = []
        self.offers = []
    
    def start_requests(self):
        """Override to add random delays and proper headers"""
        for url in self.start_urls:
            # Add random delay to simulate human browsing
            yield scrapy.Request(
                url,
                callback=self.parse,
                headers={
                    'User-Agent': self.get_random_user_agent(),
                    'Referer': 'https://www.google.com/',
                },
                dont_obey_robotstxt=False,
                meta={'dont_cache': True}
            )
    
    def get_random_user_agent(self):
        """Return a random user agent to avoid bot detection"""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        ]
        return random.choice(user_agents)
    
    def parse(self, response):
        """
        Parse the main page to extract coupons and offers
        """
        self.logger.info(f'Parsing: {response.url}')
        
        # Extract all coupon containers
        coupon_items = response.css('article.coupon-code, div.coupon-item')
        
        # If specific selectors don't work, try to extract from the page structure
        if not coupon_items:
            # Fallback: extract from divs containing coupon information
            coupon_items = response.xpath('//div[contains(@class, "coupon") or contains(@class, "promo")]')
        
        # Parse coupons with code/expiry info
        coupons_parsed = 0
        for item in response.xpath('//h3[following-sibling::*[contains(text(), "SEE PROMO CODE") or contains(text(), "GET DEAL")]]'):
            try:
                description = item.xpath('./text()').get('').strip()
                
                # Get the parent container to find code and expiry
                parent = item.xpath('./../..')
                code_text = parent.xpath('.//text()[contains(., "OFF") or contains(., "CREDITS") or contains(., "GIFTCARD")]').getall()
                expiry_text = parent.xpath('.//text()[contains(., "/")]').getall()
                
                coupon_code = next((t.strip() for t in code_text if 'OFF' in t or 'CREDITS' in t or 'GIFTCARD' in t), 'N/A')
                expiry_date = next((t.strip() for t in expiry_text if '/' in t and len(t) <= 15), 'N/A')
                
                if description:
                    self.coupons.append({
                        'type': 'coupon',
                        'description': description,
                        'code': coupon_code,
                        'expiry_date': expiry_date,
                        'scraped_at': datetime.now().isoformat()
                    })
                    coupons_parsed += 1
            except Exception as e:
                self.logger.warning(f'Error parsing coupon: {e}')
                continue
        
        self.logger.info(f'Parsed {coupons_parsed} coupons')
        
        # Log and save results
        self.logger.info(f'Total coupons found: {len(self.coupons)}')
        
        # Parse using BeautifulSoup as fallback for better results
        yield self.parse_with_text(response)
    
    def parse_with_text(self, response):
        """
        Alternative parsing method using text content
        This is more reliable for dynamic content
        """
        # Extract all text nodes containing titles and relevant info
        all_text = response.xpath('//text()').getall()
        
        coupon_patterns = []
        offer_patterns = []
        
        # Look for patterns in the extracted text
        for i, text in enumerate(all_text):
            text_lower = text.lower().strip()
            
            # Check if this looks like a coupon/offer title
            if any(keyword in text_lower for keyword in ['enjoy', 'save', 'get', 'book', 'take', 'claim', 'pay', 'score', 'grab', 'apply', 'redeem', 'spend', 'discover', 'explore', 'refer', 'stay']):
                if len(text) > 10 and len(text) < 250:
                    # Look ahead for code and expiry
                    code = 'N/A'
                    expiry = 'N/A'
                    
                    # Check next few items for code (OFF, %)
                    for j in range(i+1, min(i+10, len(all_text))):
                        next_text = all_text[j].strip()
                        if 'OFF' in next_text or 'CREDITS' in next_text or 'GIFTCARD' in next_text:
                            code = next_text
                            break
                        if '/' in next_text and len(next_text) <= 15:
                            expiry = next_text
                    
                    # If we found code or expiry, it's likely a coupon
                    if code != 'N/A' and expiry != 'N/A':
                        coupon_patterns.append({
                            'type': 'coupon',
                            'description': text.strip(),
                            'code': code,
                            'expiry_date': expiry,
                            'scraped_at': datetime.now().isoformat()
                        })
                    elif code != 'N/A':
                        offer_patterns.append({
                            'type': 'offer',
                            'description': text.strip(),
                            'discount': code,
                            'scraped_at': datetime.now().isoformat()
                        })
        
        # Remove duplicates
        seen = set()
        unique_coupons = []
        for coupon in coupon_patterns:
            key = (coupon['description'], coupon['code'])
            if key not in seen:
                seen.add(key)
                unique_coupons.append(coupon)
        
        # Yield all extracted items
        for coupon in unique_coupons:
            yield coupon
