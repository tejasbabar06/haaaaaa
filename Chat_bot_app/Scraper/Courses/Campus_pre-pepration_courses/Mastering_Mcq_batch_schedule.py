from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://sunbeaminfo.in/modular-courses.php?mdid=57")

wait = WebDriverWait(driver, 20)

wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//table[contains(@class,'table-bordered')]")
    )
)

rows = driver.find_elements(
    By.XPATH, "//table[contains(@class,'table-bordered')]//tbody/tr"
)

with open("Mastering_Mcq_batch_schedule.txt", "w", encoding="utf-8") as file:
    file.write("BATCH SCHEDULE \n")
    file.write("=" * 55 + "\n\n")

    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) < 4:
            continue
        values = []
        for td in cols:
            val = driver.execute_script(
                "return arguments[0].innerText;", td
            ).strip()
            values.append(val)
        batch_no = values[0]
        course   = values[1]
        start_dt = values[2]
        end_dt   = values[3]
        file.write(f"Batch No    : {batch_no}\n")
        file.write(f"Course Name: {course}\n")
        file.write(f"Start Date : {start_dt}\n")
        file.write(f"End Date   : {end_dt}\n")
        file.write("-" * 45 + "\n")

try:
    link = driver.find_element(
        By.XPATH, "//a[contains(text(),'Click to Register')]"
    ).get_attribute("href")
except:
    link = "Not Available"

with open("Pre_cat_CourseContent.txt", "a", encoding="utf-8") as file:
    file.write("\nRegister Link:\n")
    file.write(link)

driver.quit()

print("Data scraped successfully!")
