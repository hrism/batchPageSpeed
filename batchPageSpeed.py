import os
import asyncio
import aiohttp
import sqlite3
from datetime import datetime
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("LIGHTHOUSE_API_KEY")
API_URL = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"

def initialize_database():
    """Creates or connects to an SQLite database."""
    db_path = "/your_path/pagespeed_results.db"
    conn = sqlite3.connect(db_path)
    return conn

def create_table(conn):
    """Create a table with a unique name based on the current timestamp."""
    table_name = datetime.now().strftime("results_%Y_%m_%d_%H%M%S")
    cursor = conn.cursor()
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY,
            url TEXT NOT NULL,
            strategy TEXT NOT NULL,
            performance FLOAT,
            accessibility FLOAT,
            best_practices FLOAT,
            seo FLOAT,
            first_contentful_paint TEXT,
            speed_index TEXT,
            interactive TEXT,
            first_meaningful_paint TEXT,
            cumulative_layout_shift TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    return table_name

async def fetch_pagespeed(session, url_entry):
    """Fetch PageSpeed results for a given URL and strategy."""
    url_id = url_entry["id"]
    url = url_entry["url"]
    strategy = "mobile"
    print(f"Fetching PageSpeed data for ID: {url_id}, URL: {url}, Strategy: {strategy}")
    params = {
        "url": url,
        "key": API_KEY,
        "strategy": strategy,
        "category": ["performance", "accessibility", "seo", "best-practices"]
    }
    async with session.get(API_URL, params=params) as response:
        if response.status != 200:
            error_detail = await response.text()
            print(f"Failed to fetch {url} with status code {response.status}. Detail: {error_detail}")
            return url_id, url, strategy, None, None, None, None, None, None, None, None, None
        result = await response.json()
        lighthouse_result = result.get("lighthouseResult", {})
        categories = lighthouse_result.get("categories", {})
        audits = lighthouse_result.get("audits", {})

        performance = categories.get("performance", {}).get("score")
        accessibility = categories.get("accessibility", {}).get("score")
        best_practices = categories.get("best-practices", {}).get("score")
        seo = categories.get("seo", {}).get("score")

        fcp = audits.get("first-contentful-paint", {}).get("displayValue")
        speed_index = audits.get("speed-index", {}).get("displayValue")
        interactive = audits.get("interactive", {}).get("displayValue")
        fmp = audits.get("first-meaningful-paint", {}).get("displayValue")
        cls = audits.get("cumulative-layout-shift", {}).get("displayValue")

        print(f"Fetched data for ID: {url_id}, URL: {url}: Performance={performance}, Accessibility={accessibility}, SEO={seo}")
        return url_id, url, strategy, performance, accessibility, best_practices, seo, fcp, speed_index, interactive, fmp, cls

async def process_urls(urls):
    """Fetch PageSpeed data for multiple URLs and save results to the database."""
    print("Initializing database...")
    conn = initialize_database()
    table_name = create_table(conn)
    print(f"Created table: {table_name}")

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_pagespeed(session, entry) for entry in urls]

        results = await asyncio.gather(*tasks)  # Gather ensures results maintain order
        for result in sorted(results, key=lambda x: x[0]):  # Sort by ID
            try:
                (url_id, url, strategy, performance, accessibility, best_practices, seo,
                 fcp, speed_index, interactive, fmp, cls) = result
                if performance is not None:
                    cursor = conn.cursor()
                    cursor.execute(f'''
                        INSERT INTO {table_name} (
                            id, url, strategy, performance, accessibility, best_practices, seo,
                            first_contentful_paint, speed_index, interactive,
                            first_meaningful_paint, cumulative_layout_shift
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (url_id, url, strategy, performance, accessibility, best_practices, seo,
                          fcp, speed_index, interactive, fmp, cls))
                    conn.commit()
                    print(f"Saved result for {url} (ID: {url_id}): Performance={performance}")
                else:
                    print(f"No performance data for {url} (ID: {url_id})")
            except Exception as e:
                print(f"Error processing task for ID {result[0]}: {e}")

    conn.close()
    print("All tasks completed and database connection closed.")

if __name__ == "__main__":
    # URLs to test
    urls_to_test = [
        {"id": 1, "url": "https://example0.com/"},
        {"id": 2, "url": "https://example1.com/"},
        {"id": 3, "url": "https://example2.com/"},
        {"id": 4, "url": "https://example3.com/"},
        {"id": 5, "url": "https://example4.com/"},
        {"id": 6, "url": "https://example5.com/"},
        {"id": 7, "url": "https://example6.com/"},
        {"id": 8, "url": "https://example7.com/"},
        {"id": 9, "url": "https://example8.com/"},
        {"id": 10, "url": "https://example9.com/"},
    ]

    print("Starting PageSpeed data fetching process...")
    asyncio.run(process_urls(urls_to_test))
    print("Process completed.")
