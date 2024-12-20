# For scraping job data from Jobbix.co
# Jobbix.co is a job board website that also provides a range of custom filters

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
from dotenv import load_dotenv

load_dotenv()

driver_path = os.getenv('CHROMEDRIVER_PATH')
service = webdriver.ChromeService(executable_path=driver_path)
driver = webdriver.Chrome(service = service)

driver.get("https://jobbix.co")

# 1) Sign in to Jobbix
try:
    # Click "Sign In" button 
    sign_in_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.bg-accent.text-accent-foreground"))
    )
    sign_in_button.click()

    # Login is a modal on this website
    # Wait for the modal to appear by locating the email input field and enter data

    email_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, "email"))  
    )
    
    email_field.send_keys(os.getenv('EMAIL'))
    password_field = driver.find_element(By.NAME, "password")  
    password_field.send_keys(os.getenv('JOBBIX_PASS'))
    password_field.send_keys(Keys.RETURN)

    # To wait for login to complete 
    time.sleep(1)

except Exception as e:
    print("Error during login:", e)
    driver.quit()
    exit()

# 2) Navigate to the jobs page
driver.get("https://jobbix.co/jobs")
time.sleep(3.5)  

# A list of dictionaries to store job data, with keys "Company", "Title", and "Description"
jobs_data = []

# 3) Extract job details, repeating until all jobs are scraped
more_jobs = True
while more_jobs:

    # 3.a) Extract job details from the current page
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    jobs = soup.find_all('div', class_='text-card-foreground shadow-sm transition-colors duration-300 ease-in-out border-1 drop-shadow-sm rounded-md bg-primary flex flex-col p-2 gap-2 cursor-pointer hover:bg-secondary/30 hover:opacity-80 hover:shadow-md')  

    print(f"${len(jobs)} jobs found")

    for job in jobs:
        try:
            company = job.find_all("div", class_="text-sm", recursive=True, limit=2)
            title_text = company[0].get_text(strip=True) if len(company) > 0 else "N/A"
            company_text = company[1].get_text(strip=True) if len(company) > 1 else "N/A"
            
            print("Attempting to click job:", title_text)
            # Find the element to click using the job title
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, ".//*[contains(text(),'" + title_text + "')]"))).click()

            # Refresh the soup object after the click because the info loads in on the right side
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            # Extract job description from the sidebar
            description_div = soup.find('div', attrs={'role': 'tabpanel', 'id': True, 'class': 'mt-2'})
            # print(description_div)
            description = description_div.get_text(strip=True) if description_div else "N/A"
            
            # Add the job data to list
            jobs_data.append({
                "Company": company_text,
                "Title": title_text,
                "Description": description
            })


        except Exception as e:
            print("Error scraping job:", e)

    # 3.b) Click the "More" button to load more jobs
    try:
        more_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='More']"))   
            # This will break if the text changes but I think text is less likely to change than the tailwind classes
        )
        more_button.click()
        print("Clicked 'More'")

        # Wait for more jobs to load
        time.sleep(2)  

    except Exception:
        print("Finished scraping")
        more_jobs = False

# Saving the job data to a CSV file
df = pd.DataFrame(jobs_data)
df.to_csv("Dataset/jobs.csv", index=False, mode="a", header=False)
print("Job data saved to jobs.csv")

driver.quit()



