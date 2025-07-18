# Import required libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# Set up Chrome options (detach keeps the browser open after script ends)
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

# Launch the Chrome driver
driver = webdriver.Chrome(options=options)

# Set up an explicit wait
wait = WebDriverWait(driver, 15)

print("Opening Internshala internships page...")
# Navigate to Internshala's work-from-home internships page for Mumbai
driver.get("https://internshala.com/internships/work-from-home-internships-in-mumbai/")
driver.maximize_window()  # Maximize browser window for better element visibility

# Close the initial popup if it appears
try:
    close_btn = wait.until(EC.element_to_be_clickable((By.ID, "close_popup")))
    close_btn.click()
    print("Closed popup.")
except:
    print("No popup appeared.")

# Initialize job data list and page counter
job_data = []
page = 1

# Start scraping loop
while True:
    print(f"\n📄 Scraping Page {page}...")

    # Wait for the job listings container to load
    container = wait.until(EC.presence_of_element_located((By.ID, "reference")))

    # Find all job blocks within the container
    job_blocks = container.find_elements(By.XPATH, ".//div[contains(@class,'individual_internship')]")

    new_jobs = 0  # Counter to track jobs scraped in this page

    # Loop through each job block and extract data
    for job in job_blocks:
        try:
            title_element = job.find_element(By.XPATH, ".//a[@class='job-title-href']")
            title = title_element.text.strip()
            link = title_element.get_attribute("href")
        except:
            continue  # Skip job if title/link not found

        try:
            company = job.find_element(By.XPATH, ".//p[contains(@class,'company-name')]").text.strip()
        except:
            company = "N/A"  # Fallback if company not found

        try:
            stipend = job.find_element(By.XPATH, ".//span[@class='stipend']").text.strip()
        except:
            stipend = "N/A"  # Fallback if stipend not found

        try:
            duration = job.find_element(By.XPATH, ".//div[@class='row-1-item'][.//i[contains(@class, 'ic-16-calendar')]]").text.strip()
        except:
            duration = "N/A"  # Fallback if duration not found

        # Append extracted job data to the list
        job_data.append({
            "Title": title,
            "Company": company,
            "Stipend": stipend,
            "Duration": duration,
            "Link": link
        })

        new_jobs += 1

    print(f"✅ Page {page} scraped. Jobs added: {new_jobs}. Total: {len(job_data)}")

    # Attempt to go to the next page
    try:
        current_url = driver.current_url
        next_button = wait.until(EC.element_to_be_clickable((By.ID, "navigation-forward")))
        driver.execute_script("arguments[0].click();", next_button)
        time.sleep(2)  # Wait for new page to load
        new_url = driver.current_url

        # Break loop if page doesn't change (end of listings)
        if new_url == current_url:
            print("🚫 No change in URL after clicking Next. Breaking loop.")
            break

        page += 1
    except:
        print("❌ Next button not found or not clickable. Exiting loop.")
        break

# Convert scraped job data to a pandas DataFrame
df = pd.DataFrame(job_data)

# Save the data to a CSV file
df.to_csv("internshala_jobs.csv", index=False, encoding="utf-8")
print("💾 Data saved to internshala_jobs.csv")

# Wait a few seconds and then close the browser
time.sleep(3)
driver.quit()
print("👋 Browser closed. Scraping completed successfully.")
