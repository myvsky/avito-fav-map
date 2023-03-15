import csv
import browsercookie
from selenium import webdriver
from selenium.webdriver.common.by import By

# Import data from your physical browser
cj = browsercookie.chrome()

driver = webdriver.Chrome()
url = "https://avito.ru/favorites"
driver.get(url)

# Apply cookies for avito.ru from your physical browser to webdriver
for cookie in cj:
    # Apply cookies for domain we're in
    if cookie.domain == ".avito.ru" or cookie.domain == ".www.avito.ru":
        driver.add_cookie(({
            'name': cookie.name,
            'value': cookie.value,
            'domain': cookie.domain,
            'path': cookie.path,
            'expires': cookie.expires
    }))
# Refresh webpage, apply cookies
driver.get(url)

# Find all addresses
elements = driver.find_elements(By.CLASS_NAME, "location-addressLine-fHEor")

# Convert webobjects to the list
elements = [i.text for i in elements]

with open("data.csv", mode="w", encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Адреса"])
    for element in elements:
        writer.writerow([element])

print("CSV файл с адресами появился в текущей директории")
driver.quit()
