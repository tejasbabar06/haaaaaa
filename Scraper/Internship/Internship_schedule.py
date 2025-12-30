from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.sunbeaminfo.in/internship")

info_list = []

# NOTE: table loads dynamically → this works because table is already visible
table_rows = driver.find_elements(By.XPATH, '//div//table//tbody/tr')

for rows in table_rows:
    col = rows.find_elements(By.XPATH, './/td')

    if len(col) == 8:
        info = {
            "Batch": col[1].text.strip(),
            "Batch Duration": col[2].text.strip(),
            "Start Date": col[3].text.strip(),
            "End Date": col[4].text.strip(),
            "Time": col[5].text.strip(),
            "Fees": col[6].text.strip(),
            "Download": col[7].text.strip()
        }
        info_list.append(info)

driver.quit()
with open("internship_schedule.txt", "w", encoding="utf-8") as f:
    for i, item in enumerate(info_list, start=1):
        f.write(f"Record {i}\n")
        for key, value in item.items():
            f.write(f"{key}: {value}\n")
        f.write("-" * 40 + "\n")

print("Data saved to internship_schedule.txt")
