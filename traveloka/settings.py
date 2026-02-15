# Scrapy settings for traveloka project

BOT_NAME = 'traveloka'
SPIDER_MODULES = ['traveloka.spiders']
NEWSPIDER_MODULE = 'traveloka.spiders'

# Crawl responsibly by identifying yourself (optional)
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

# Respect robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests per domain
CONCURRENT_REQUESTS = 16

# Configure a delay for requests for the same website
DOWNLOAD_DELAY = 2  # 2 second delay between requests

# Disable cookies to appear more like a browser
COOKIES_ENABLED = False

# Maximum retries
RETRY_TIMES = 3

# Set custom headers to mimic real browser
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0',
}

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# AutoThrottle settings
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 2
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_TARGET_CONCURRENCY = 2.0
AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching to avoid re-downloading pages
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0  # Don't use cache for freshness

# Configure item pipelines
ITEM_PIPELINES = {
    'traveloka.pipelines.TravelokaPipeline': 300,
}

# Export settings
FEEDS = {
    'output/coupons.jsonl': {
        'format': 'jsonl',
    },
}

# Disable Telnet console
TELNETCONSOLE_ENABLED = False

# Log settings
LOG_LEVEL = 'INFO'
