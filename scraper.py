import sys
import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import db_setup  # Import to ensure database exists

sys.stdout.reconfigure(encoding="utf-8")

def get_job_count(job_type):
    con = sqlite3.connect("jobsNumbers.db")
    cur = con.cursor()

    chrome_options = Options()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

    driver = webdriver.Chrome(options=chrome_options)

    try:
        job_urls = {
            "pythonIndeed": "https://mx.indeed.com/jobs?q=python&l=mexico&sc=0kf%3Aattr%28DSQF7%29%3B&from=searchOnDesktopSerp",
            "javascriptIndeed": "https://mx.indeed.com/jobs?q=javascript&l=mexico&sc=0kf%3Aattr%28DSQF7%29%3B&from=searchOnDesktopSerp"
        }

        if job_type not in job_urls:
            print(f"⚠️ Invalid job type: {job_type}")
            return None

        driver.get(job_urls[job_type])

        wait = WebDriverWait(driver, 10)
        job_count_element = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "div.jobsearch-JobCountAndSortPane-jobCount span")
        ))

        job_count = int(job_count_element.text.replace("+", "").split()[0])
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(f"✅ Scraped Job Count: {job_type} → {job_count}")

        # Insert into SQLite using a parameterized query
        cur.execute("""
            INSERT INTO AtJobsHist (jobType, JobNumber, TimeStamp) 
            VALUES (?, ?, ?)
        """, (job_type, job_count, timestamp))

        con.commit()
        print(f"✅ Inserted into DB: {job_type} → {job_count} at {timestamp}")

        # Retrieve all data after inserting to verify
        cur.execute("SELECT * FROM AtJobsHist ORDER BY ID DESC LIMIT 5")
        results = cur.fetchall()
        print("📌 Latest 5 records from DB:")
        for row in results:
            print(row)

    except Exception as e:
        print(f"❌ Error: {e}")

    finally:
        driver.quit()
        con.close()

if __name__ == "__main__":
    db_setup.setup_database()  # Ensure DB exists before running scraper
    get_job_count("pythonIndeed")
    get_job_count("javascriptIndeed")
