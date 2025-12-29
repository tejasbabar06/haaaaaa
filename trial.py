from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, os

# ------------------ SETUP ------------------
os.makedirs("data", exist_ok=True)

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

# ------------------ STEP 1: GET ALL LINKS FROM SITEMAP ------------------
driver.get("https://sunbeaminfo.in/sitemap")
time.sleep(3)

all_links = []
for a in driver.find_elements(By.TAG_NAME, "a"):
    href = a.get_attribute("href")
    if href and href.startswith("https://sunbeaminfo.in/modular-courses"):
        all_links.append(href)

all_links = list(set(all_links))
print(f"Total course links found: {len(all_links)}")

# ------------------ STEP 2: SCRAPE ALL LINKS ------------------
output_path = "data/sunbeam_all_courses_FINAL.txt"

with open(output_path, "w", encoding="utf-8") as out:

    for idx, url in enumerate(all_links, start=1):
        print(f"\n[{idx}/{len(all_links)}] Scraping: {url}")

        try:
            driver.get(url)
            time.sleep(3)

            out.write("\n" + "=" * 120 + "\n")
            out.write(f"URL: {url}\n")
            out.write("=" * 120 + "\n")

            # 🔹 Basic visible info
            for el in driver.find_elements(By.XPATH, "//h1 | //h2 | //h3 | //p"):
                text = el.text.strip()
                if text:
                    out.write(text + "\n")

            # 🔥 ACCORDION FIX (WORKING LOGIC)
            accordion_links = driver.find_elements(
                By.XPATH,
                "//a[contains(@data-toggle,'collapse') and contains(@href,'#collapse')]"
            )

            for acc in accordion_links:
                section_title = acc.text.strip()

                try:
                    collapse_id = acc.get_attribute("href").split("#")[-1]

                    driver.execute_script("arguments[0].scrollIntoView(true);", acc)
                    driver.execute_script("arguments[0].click();", acc)

                    panel = wait.until(
                        EC.visibility_of_element_located((By.ID, collapse_id))
                    )

                    time.sleep(0.5)

                    out.write("\n" + section_title.upper() + "\n")
                    out.write("-" * 60 + "\n")

                    items = panel.find_elements(By.XPATH, ".//li | .//p | .//td")

                    for item in items:
                        txt = item.text.strip()
                        if txt:
                            out.write(txt + "\n")

                except Exception as e:
                    print(f"  Skipped section: {section_title}")

        except Exception as e:
            print(f"❌ Failed to scrape {url}: {e}")

driver.quit()
print("\n✅ ALL COURSE PAGES SCRAPED SUCCESSFULLY")
