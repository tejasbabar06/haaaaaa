from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.sunbeaminfo.in/internship")

# 🔥 Select the full course card, NOT course_info
course_cards = driver.find_elements(
    By.CSS_SELECTOR, "div.single_course"
)

with open("Apache_spark_course_details.txt", "w", encoding="utf-8") as f:
    count = 0
    for card in course_cards:
        text = card.get_attribute("innerText").strip()
        if text:
            count += 1
            f.write(f"Course {count}\n")
            f.write(text + "\n")
            f.write("-" * 50 + "\n")

driver.quit()

print(f"✅ {count} course blocks scraped successfully")
