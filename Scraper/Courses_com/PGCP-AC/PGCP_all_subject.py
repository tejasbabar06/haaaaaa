from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-gpu")

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.sunbeaminfo.com/post-graduate-diploma-programmes/PG-DAC")

# Wait for page load
WebDriverWait(driver, 30).until(
    lambda d: d.execute_script("return document.readyState") == "complete"
)

# -------------------------------
# Extract subject names + content
# -------------------------------
subjects = driver.execute_script("""
    let result = [];

    let headings = document.querySelectorAll("h4, h3");
    let contents = document.querySelectorAll("div.list_style p");

    let count = Math.min(headings.length, contents.length);

    for (let i = 0; i < count; i++) {
        let title = headings[i].innerText.trim();
        let text = contents[i].innerText.trim();

        result.push({
            title: title,
            content: text
        });
    }

    return result;
""")

# -------------------------------
# Extract PDF link
# -------------------------------
pdf_link = driver.execute_script("""
    let pdf = document.querySelector("a.download_pdf_btn");
    return pdf ? pdf.href : "Not Available";
""")

# -------------------------------
# Write to file
# -------------------------------
with open("PGCP_All_Subjects.txt", "w", encoding="utf-8") as file:
    file.write("PG-DAC COURSE CONTENT\n")
    # file.write("=" * 40 + "\n\n")

    for sub in subjects:
        file.write(sub["title"].upper() + "\n")
        # file.write("-" * len(sub["title"]) + "\n")
        file.write(sub["content"] + "\n\n")

    file.write("Admission Booklet PDF:\n")
    file.write(pdf_link)

driver.quit()
print("Subjects scraped with proper names")
