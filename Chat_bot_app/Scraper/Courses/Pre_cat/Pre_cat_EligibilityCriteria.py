from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://sunbeaminfo.in/pre-cat")

# Get visible eligibility text
eligibility = driver.execute_script("""
    let text = "";
    document.querySelectorAll("div.list_style ul li").forEach(li => {
        if (li.innerText.trim() !== "") {
            text = li.innerText.trim();
        }
    });
    return text;
""")

# Get register link
register_link = driver.find_element(
    By.XPATH, "//a[contains(text(),'Click to Register')]"
).get_attribute("href")

# Write output
with open("Pre_cat_EligibilityCriteria.txt", "w", encoding="utf-8") as f:
    f.write("ELIGIBILITY CRITERIA - PRE CAT\n")
    f.write("=" * 50 + "\n\n")
    f.write(f"1. {eligibility}\n\n")
    f.write("Register Link:\n")
    f.write(register_link)

driver.quit()
