from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# -------------------------------
# Chrome Setup
# -------------------------------
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-gpu")

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.sunbeaminfo.com/post-graduate-diploma-programmes/PG-DAC")

# -------------------------------
# Wait for page to fully load
# -------------------------------
WebDriverWait(driver, 30).until(
    lambda d: d.execute_script("return document.readyState") == "complete"
)

# -------------------------------
# Extract text DIRECTLY via JS
# -------------------------------
course_text = driver.execute_script("""
    let el = document.querySelector("div.list_style p");
    return el ? el.innerText.trim() : "";
""")

# -------------------------------
# Extract PDF link (SAFE)
# -------------------------------
pdf_link = driver.execute_script("""
    let pdf = document.querySelector("a.download_pdf_btn");
    return pdf ? pdf.href : "Not Available";
""")

# -------------------------------
# Write to file
# -------------------------------
with open("PGCP_concept_os.txt", "w", encoding="utf-8") as file:
    file.write("CONCEPT OF OPERATING SYSTEM\n")
    file.write("=" * 40 + "\n\n")
    file.write(course_text + "\n\n")
    file.write("Admission Booklet PDF:\n")
    file.write(pdf_link)

driver.quit()

print("✅ SCRAPING COMPLETED SUCCESSFULLY")
