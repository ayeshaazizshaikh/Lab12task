# pip install selenium   (Selenium 4.6+ downloads the driver automatically)
import os, sys
from selenium import webdriver
from selenium.webdriver.common.by import By

URL = "file:///" + os.path.abspath("index.html").replace("\\", "/")

# (input, expected result)
CASES = [("-1", "Rejected"), ("0", "Accepted"), ("5", "Accepted"),
         ("10", "Accepted"), ("11", "Rejected")]

driver = webdriver.Chrome()
rows = []
try:
    for value, expected in CASES:
        driver.get(URL)
        driver.find_element(By.ID, "mark").send_keys(value)
        driver.find_element(By.ID, "submit").click()
        actual = driver.find_element(By.ID, "result").text
        ok = actual.startswith(expected)
        rows.append((value, expected, actual, "PASS" if ok else "FAIL"))

    # Targeted check for the improvement: message must state the range
    driver.get(URL)
    driver.find_element(By.ID, "mark").send_keys("11")
    driver.find_element(By.ID, "submit").click()
    msg = driver.find_element(By.ID, "result").text
    rows.append(("11 (message)", "mentions '0 to 10'", msg,
                 "PASS" if "0 to 10" in msg else "FAIL"))
finally:
    driver.quit()

print(f"{'Input':<14}{'Expected':<20}{'Actual':<48}Result")
for r in rows:
    print(f"{r[0]:<14}{r[1]:<20}{r[2]:<48}{r[3]}")
sys.exit(0 if all(r[3] == "PASS" for r in rows) else 1)
