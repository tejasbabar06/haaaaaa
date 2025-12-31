from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://sunbeaminfo.in/modular-courses.php?mdid=57")  
driver.implicitly_wait(5)

print("Page Title:", driver.title)

elements = driver.find_elements(By.CLASS_NAME, "course_info")

with open("Mastering_Mcq_Course_details.txt", "w", encoding="utf-8") as f:
    for el in elements:
        text = el.text.strip()
        if text:
            f.write(text)
            f.write("\n" + "-"*40 + "\n")

driver.quit()
