from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

# Chrome setup
chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)

# Open page
driver.get("https://www.sunbeaminfo.in/internship")
print("Page Title:", driver.title)

# Wait for the specific collapse div
wait = WebDriverWait(driver, 10)
element = wait.until(
    EC.presence_of_element_located(
        (By.ID, "collapseFour")
    )
)

# Extract text safely
text = element.get_attribute("innerText").strip()



with open("Benifits_internship.txt", "w", encoding="utf-8") as f:
    if text:
        f.write(text)

print("Data saved to Internship_CollapseFour.txt")

driver.quit()
