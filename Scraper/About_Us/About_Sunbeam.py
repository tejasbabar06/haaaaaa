from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

driver.get("https://www.sunbeaminfo.in/about-us")
print("Page Title:", driver.title)
driver.implicitly_wait(5)

elements = driver.find_elements(By.CLASS_NAME, "main_info")

with open("About_Sunbeam.txt", "w", encoding="utf-8") as f:
    for el in elements:
        text = el.text.strip()
        if text:
            f.write(text + "\n\n")
driver.quit()
