from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://sunbeaminfo.in/pre-cat")

wait = WebDriverWait(driver, 15)

# Get all li elements
list_items = wait.until(
    EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "div.list_style ul li")
    )
)

# Get register link
register_btn = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//a[contains(text(),'Register')]")
    )
)

with open("Pre_cat_CourseContent.txt", "w", encoding="utf-8") as file:
    file.write("SUNBEAM PRE-CAT COURSE CONTENT\n")
    file.write("=" * 40 + "\n\n")

    for i, li in enumerate(list_items, 1):
        text = driver.execute_script(
            "return arguments[0].innerText;", li
        ).strip()

        if text:
            file.write(f"{i}. {text}\n")

    file.write("\nRegister Link:\n")
    file.write(register_btn.get_attribute("href"))

driver.quit()
