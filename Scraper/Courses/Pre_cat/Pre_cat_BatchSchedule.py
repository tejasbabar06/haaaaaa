from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://sunbeaminfo.in/pre-cat")

wait = WebDriverWait(driver, 20)

# 🔴 VERY IMPORTANT — wait for table to load fully
wait.until(EC.presence_of_element_located(
    (By.XPATH, "//table[contains(@class,'table-bordered')]")
))

time.sleep(2)  # allow JS to inject data

rows = driver.find_elements(
    By.XPATH, "//table[contains(@class,'table-bordered')]//tbody/tr"
)

with open("Pre_cat_BatchSchedule.txt", "w", encoding="utf-8") as f:
    f.write("PRE-CAT BATCH SCHEDULE\n")
    f.write("=" * 55 + "\n\n")

    for row in rows:
        # get inner HTML (important)
        tds = row.find_elements(By.TAG_NAME, "td")

        if len(tds) < 7:
            continue

        values = []
        for td in tds:
            val = driver.execute_script(
                "return arguments[0].innerText;", td
            ).replace("\n", " ").strip()
            values.append(val)

        f.write(f"Batch No     : {values[0]}\n")
        f.write(f"Batch Code   : {values[1]}\n")
        f.write(f"Duration     : {values[2]}\n")
        f.write(f"Start Date   : {values[3]}\n")
        f.write(f"End Date     : {values[4]}\n")
        f.write(f"Timing       : {values[5]}\n")
        f.write(f"Fees         : {values[6]}\n")
        f.write("-" * 45 + "\n")

# Register link
try:
    link = driver.find_element(
        By.XPATH, "//a[contains(text(),'Click to Register')]"
    ).get_attribute("href")
except:
    link = "Not Available"

with open("Pre_cat_BatchSchedule.txt", "a", encoding="utf-8") as f:
    f.write("\nRegister Link:\n")
    f.write(link)

driver.quit()

print("✅ Output generated successfully!")
