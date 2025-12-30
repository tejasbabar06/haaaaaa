import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def scrape_modular_courses(URL, course_name, output_filename):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    try:
        driver.get(URL)
        wait = WebDriverWait(driver, 20)

        course_data = {
            "course_name": course_name,
            "url": URL,
            "general_info": "",
            "sections": [],
            "batch_schedule_table": []
        }
        try:
            info_container = driver.find_element(By.CLASS_NAME, "course_info")
            course_data["general_info"] = info_container.text.strip()
        except:
            course_data["general_info"] = "Summary section not found"

        headers = wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "panel-heading"))
        )

        ALLOWED_SECTIONS = {
            "syllabus",
            "pre requisites",
            "pre-requisites",
            "outcome",
            "software setup"
        }

        for i in range(len(headers)):
            current_headers = driver.find_elements(By.CLASS_NAME, "panel-heading")
            header = current_headers[i]
            title = header.text.strip()

            link = header.find_element(By.TAG_NAME, "a")
            driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});", link
            )
            time.sleep(1)
            driver.execute_script("arguments[0].click();", link)
            time.sleep(2)

            if "Batch" in title:
                try:
                    table = driver.find_element(
                        By.CSS_SELECTOR,
                        ".panel-collapse.collapse.in table"
                    )
                    table_headers = [
                        th.text.strip()
                        for th in table.find_elements(By.TAG_NAME, "th")
                    ]
                    rows = table.find_elements(By.TAG_NAME, "tr")[1:]

                    for row in rows:
                        cells = row.find_elements(By.TAG_NAME, "td")
                        if cells:
                            row_data = {
                                table_headers[j]: cells[j].text.strip()
                                for j in range(min(len(table_headers), len(cells)))
                            }
                            course_data["batch_schedule_table"].append(row_data)
                except:
                    pass

            else:
                try:
                    body = driver.find_element(
                        By.CSS_SELECTOR,
                        ".panel-collapse.collapse.in .panel-body"
                    )

                    clean_title = (
                        title.replace(":", "")
                             .replace("-", " ")
                             .strip()
                             .lower()
                    )

                    if clean_title in ALLOWED_SECTIONS:
                        course_data["sections"].append({
                            "title": title.replace(":", "").strip(),
                            "content": body.text.strip()
                        })
                except:
                    pass

        with open(output_filename, "w", encoding="utf-8") as f:
            f.write("GENERAL INFORMATION\n")
            f.write(course_data["general_info"] + "\n\n")

            f.write("COURSE DETAILS\n")
            for section in course_data["sections"]:
                f.write(f"\n[{section['title']}]\n")
                f.write(section["content"] + "\n")

            if course_data["batch_schedule_table"]:
                f.write("\n\nBATCH SCHEDULE\n")
                for idx, batch in enumerate(course_data["batch_schedule_table"], 1):
                    f.write(f"\nBatch {idx}\n")
                    for k, v in batch.items():
                        f.write(f"{k} : {v}\n")

        print(f"✔ Saved TXT → {output_filename}")

    finally:
        driver.quit()
