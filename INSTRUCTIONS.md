# Coupon Scraper - Client Instructions

## Table of Contents
1. [Project Overview](#project-overview)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [How to Run the Project](#how-to-run-the-project)
5. [How to Change the URL for Different Stores](#how-to-change-the-url-for-different-stores)
6. [Understanding the Output Files](#understanding-the-output-files)
7. [Troubleshooting](#troubleshooting)
8. [Important Notes](#important-notes)

---

## Project Overview

This is a coupon and deals scraper that uses **Selenium** with Chrome browser to extract promotional codes and offers from the Cuponation website (Singapore version: cuponation.com.sg).

**Current Working Script:** [`scraper_fixed_modal.py`](scraper_fixed_modal.py)

**Default URL:** `https://www.cuponation.com.sg/traveloka-promo-code`

The scraper extracts two types of data:
- **Coupons** - Promotional codes that require a code (SEE PROMO CODE buttons)
- **Offers** - Deals without codes (GET DEAL buttons)

---

## Prerequisites

Before running the project, ensure you have:

- **Python 3.7 or higher** installed on your system
- **Google Chrome browser** installed (required for Selenium)
- **pip** (Python package installer)
- **Internet connection**
- A code editor (VS Code, PyCharm, or any text editor)

---

## Installation

### Step 1: Navigate to the Project Directory

Open your terminal/command prompt and navigate to the folder where you have the project files:

```bash
# Example: If you copied the project to your Desktop
cd C:\Users\maxto\OneDrive\Desktop\coupons

# Or if the project is in a different location, navigate there
cd "path\to\your\project folder"
```

**Important:** Make sure you run all commands from this folder!

### Step 2: Create a Virtual Environment (Recommended)

```bash
python -m venv .venv
```

**Note:** If you get an error about paths, see the Troubleshooting section below.

### Step 3: Activate the Virtual Environment

**On Windows (Command Prompt):**
```bash
.venv\Scripts\activate
```

**On Windows (PowerShell):**
```bash
.venv\Scripts\Activate
```

**On macOS/Linux:**
```bash
source .venv/bin/activate
```

After activation, you should see `(.venv)` at the beginning of your command prompt.

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

**If you get "Fatal error in launcher" error:**
- This means the virtual environment paths are wrong
- See the Troubleshooting section below for solutions

This will install:
- selenium==4.15.2 (Browser automation)
- webdriver-manager (Automatic Chrome driver installation)
- pyperclip (Clipboard access for copying promo codes)
- Other required packages

---

## How to Run the Project

### Running the Working Solution

The working solution uses Selenium with Chrome browser:

```bash
python scraper_fixed_modal.py
```

**What happens:**
1. Chrome browser opens (may be visible or headless)
2. Loads the Cuponation page
3. Accepts cookies automatically
4. Extracts OFFERS (Get Deal buttons - no code needed)
5. Clicks each SEE PROMO CODE button to get the actual codes
6. Extracts title, code, and expiry date for each coupon
7. Saves results to output folder

**Expected Output:**
```
Loading https://www.cuponation.com.sg/traveloka-promo-code...
Waiting for page to load...
Page loaded

=== Extracting OFFERS (GET DEAL) ===
Found 5 GET DEAL buttons
  1. Get up to 20% off on Hotel Bookings
  2. ...
Extracted 5 offers

=== Extracting COUPONS (SEE PROMO CODE) ===
Scrolling to load all coupons...
Found 38 coupons
  Clicked button 1
  Title: Save 15% off on Flight Bookings
  Code: SAVE15OFF
  Expiry: 31/12/2024
  1. SAVE15OFF      | Save 15% off on Flight Bookings | 31/12/2024
  
  Clicked button 2
  ...
Extracted 38 coupons

Saving to output/...
   coupons.json
   coupons.csv
   offers.json
   offers.csv
   traveloka_coupons.txt
   all_results.json

Total: 38 coupons, 5 offers
All files saved!
Browser closed
```

---

## How to Change the URL for Different Stores

### Understanding Cuponation URL Structure

The Cuponation website uses a consistent URL pattern:

```
https://www.cuponation.com.sg/{STORE_NAME}-promo-code
```

### Examples of Different Store URLs

| Store Name | URL |
|------------|-----|
| Traveloka | `https://www.cuponation.com.sg/traveloka-promo-code` |
| Shopee | `https://www.cuponation.com.sg/shopee-promo-code` |
| Lazada | `https://www.cuponation.com.sg/lazada-promo-code` |
| Grab | `https://www.cuponation.com.sg/grab-promo-code` |
| Amazon Singapore | `https://www.cuponation.com.sg/amazon-singapore-promo-code` |
| Zalora | `https://www.cuponation.com.sg/zalora-promo-code` |
| Qoo10 | `https://www.cuponation.com.sg/qoo10-promo-code` |
| FairPrice | `https://www.cuponation.com.sg/fairprice-promo-code` |
| Cold Storage | `https://www.cuponation.com.sg/cold-storage-promo-code` |
| Guardian | `https://www.cuponation.com.sg/guardian-promo-code` |

### How to Change the URL

1. Open [`scraper_fixed_modal.py`](scraper_fixed_modal.py) in your code editor
2. Find line 57:
   ```python
   url = "https://www.cuponation.com.sg/traveloka-promo-code"
   ```
3. Replace with your desired store URL:
   ```python
   url = "https://www.cuponation.com.sg/shopee-promo-code"
   ```
4. Save the file
5. Run the scraper:
   ```bash
   python scraper_fixed_modal.py
   ```

### Optional: Rename Output Files

If you want different output filenames for each store:

1. Open [`scraper_fixed_modal.py`](scraper_fixed_modal.py)
2. In the `save()` method (around line 328), you can modify the filenames:
   ```python
   # Change from:
   (p / 'traveloka_coupons.txt').write_text(...)
   
   # To:
   (p / 'shopee_coupons.txt').write_text(...)
   ```
3. Or manually rename the output files after scraping

### Finding the Correct URL for Any Store

1. Go to [https://www.cuponation.com.sg/](https://www.cuponation.com.sg/)
2. Search for the store you want (e.g., "Shopee")
3. Click on the store's coupon page
4. Copy the URL from your browser's address bar
5. Use that URL in the scraper

---

## Understanding the Output Files

The scraper generates several output files in the `output/` folder:

### 1. coupons.json
Contains all coupons with promo codes in JSON format.

**Structure:**
```json
[
  {
    "Title": "Save 20% off on Hotel Bookings",
    "Code": "SAVE20",
    "Expires": "31/12/2024"
  }
]
```

### 2. offers.json
Contains special offers and deals without promo codes.

**Structure:**
```json
[
  {
    "title": "Get $10 off on first booking"
  }
]
```

### 3. all_results.json
Combined summary of both coupons and offers with metadata.

**Structure:**
```json
{
  "timestamp": "2024-01-15T10:30:00",
  "total_coupons": 15,
  "total_offers": 5,
  "coupons": [...],
  "offers": [...]
}
```

### 4. coupons.csv
Excel-compatible CSV file with all coupon data.

**Columns:**
- Title
- Code
- Expires

### 5. offers.csv
Excel-compatible CSV file with all offer data.

### 6. traveloka_coupons.txt
Human-readable text report combining both offers and coupons.

---

## Troubleshooting

### Issue: "Fatal error in launcher: Unable to create process..."

**Cause:** This error occurs when the virtual environment paths are mixed up - typically when the project was copied from one location to another (e.g., from `d:\07-Data Extraction\coupons` to `C:\Users\maxto\OneDrive\Desktop\coupons`).

**Solution 1: Delete old venv and create new one (Recommended)**

```bash
# Navigate to your project folder (where you copied the project)
cd C:\Users\maxto\OneDrive\Desktop\coupons

# Delete the old virtual environment folder (if exists)
rmdir /s /q .venv

# Create a new virtual environment
python -m venv .venv

# Activate it
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Solution 2: Use System Python (No Virtual Environment)**

If you don't want to use a virtual environment:

```bash
# Navigate to your project folder
cd C:\Users\maxto\OneDrive\Desktop\coupons

# Install directly with system Python
pip install -r requirements.txt

# Run the scraper
python scraper_fixed_modal.py
```

**Solution 3: Fix by reinstalling in the correct location**

```bash
# First, find where your Python is installed
where python

# Navigate to your actual project folder (the new location)
cd C:\Users\maxto\OneDrive\Desktop\coupons

# Remove any old venv that might have wrong paths
if exist .venv rmdir /s /q .venv

# Create fresh virtual environment
python -m venv .venv

# Activate
.venv\Scripts\activate

# Install
pip install -r requirements.txt

# Run
python scraper_fixed_modal.py
```

### Issue: "ModuleNotFoundError: No module named 'selenium'"

**Solution:** Install the required packages:
```bash
pip install -r requirements.txt
```

### Issue: "Chrome not reachable" or "Chrome failed to start"

**Possible Causes:**
- Google Chrome is not installed
- Chrome version is incompatible

**Solutions:**
1. Install Google Chrome browser
2. The script uses webdriver-manager which should automatically download the correct ChromeDriver

### Issue: "Timeout waiting for page load"

**Cause:** Slow internet or website is slow to respond

**Solutions:**
1. Increase the sleep time in the script (line 62)
2. Check your internet connection
3. Try again later

### Issue: "No coupons found" or "0 coupons"

**Possible Causes:**
- Website structure has changed
- Incorrect URL
- Page didn't load properly

**Solutions:**
1. Verify the URL is correct and accessible in your browser
2. Check if the website is up and running
3. The selectors in the script may need updating

### Issue: "Element click intercepted"

**Cause:** Another element is covering the button

**Solution:** The script already handles this with JavaScript clicks, but you may need to increase sleep times

### Issue: "WebDriverException"

**Cause:** ChromeDriver version mismatch

**Solution:** The webdriver-manager should handle this automatically. If it persists:
```bash
pip install --upgrade webdriver-manager
```

---

## Important Notes

### 1. Browser Behavior
- The script currently runs Chrome in visible mode (line 40 is commented out for `--headless`)
- You can see the browser working through the scraping process
- To run in headless mode, uncomment line 40:
  ```python
  options.add_argument('--headless')
  ```

### 2. Rate Limiting
- The scraper includes delays between actions (1-5 seconds)
- This is intentional to avoid being blocked
- Do NOT remove these delays

### 3. Legal Considerations
- This scraper is for educational purposes
- Always respect the website's Terms of Service
- Do not overuse the scraper - space out your requests

### 4. Website Changes
- Cuponation may change their website structure periodically
- If scraping stops working, the selectors may need updating
- Contact the developer for updates if needed

### 5. Data Freshness
- Coupon codes expire frequently
- Always run the scraper close to when you plan to use the codes
- Check the expiry dates in the output files

### 6. Clipboard Access
- The script uses `pyperclip` to copy promo codes
- Make sure no other application is using the clipboard when running

---

## Quick Reference Card

| Task | Command |
|------|---------|
| Install dependencies | `pip install -r requirements.txt` |
| Run scraper | `python scraper_fixed_modal.py` |
| Activate virtual environment (Windows) | `.venv\Scripts\activate` |
| Activate virtual environment (Mac/Linux) | `source .venv/bin/activate` |
| Run in headless mode | Uncomment line 40 in scraper_fixed_modal.py |

---

## File Structure

```
coupons/
├── scraper_fixed_modal.py    # Main working script (Selenium)
├── main.py                   # Alternative script (not currently used)
├── requirements.txt          # Python dependencies
├── traveloka/                # Scrapy spider (not currently used)
│   ├── settings.py
│   └── spiders/
│       └── traveloka_spider.py
└── output/                   # Generated output files
    ├── coupons.json
    ├── coupons.csv
    ├── offers.json
    ├── offers.csv
    ├── traveloka_coupons.txt
    └── all_results.json
```

---

## Support

If you encounter any issues or have questions:
1. Check the troubleshooting section above
2. Verify all installation steps were completed
3. Ensure you're using the correct URL format
4. Make sure Google Chrome is installed
5. Check that you have an active internet connection

---

*Last Updated: 2024*
*Version: 2.0*
