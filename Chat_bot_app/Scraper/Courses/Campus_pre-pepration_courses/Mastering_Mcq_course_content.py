from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://sunbeaminfo.in/modular-courses.php?mdid=57")
driver.implicitly_wait(5)

print("Page Title:", driver.title)

course_btn = driver.find_element(By.CSS_SELECTOR, "a[href='#collapse302']")
driver.execute_script("arguments[0].click();", course_btn)

time.sleep(1)

content_div = driver.find_element(By.ID, "collapse302")
content_text = content_div.text.strip()

with open("Mastering_Mcq_course_content.txt", "w", encoding="utf-8") as f:
    if content_text:
        f.write("Course Contents:\n")
        f.write(content_text)

driver.quit()
