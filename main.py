import csv
import browsercookie
from selenium import webdriver
from selenium.webdriver.common.by import By

# Gain cookies from Chrome browser
cj = browsercookie.chrome()
# Use Chrome as a webdriver
driver = webdriver.Chrome()

# Collect needed data from Avito.ru
def collect_addresses(cj, driver):

    url = "https://avito.ru/favorites"
    driver.get(url)

    # Apply only cookies with Avito's domain
    for cookie in cj:
        if cookie.domain == ".avito.ru" or cookie.domain == ".www.avito.ru":
            driver.add_cookie(({
                'name': cookie.name,
                'value': cookie.value,
                'domain': cookie.domain,
                'path': cookie.path,
                'expires': cookie.expires
        }))

    # Forced page refresh
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

    print("CSV file appeared in current directory")

def apply_to_maps(cj, driver):

    url = "https://google.com/maps/d/u/0"
    driver.get(url)

    for cookie in cj:
        if cookie.domain == ".google.com":
            driver.add_cookie(({
                'name': cookie.name,
                'value': cookie.value,
                'domain': cookie.domain,
                'path': cookie.path,
                'expires': cookie.expires
        }))
    
    driver.get(url)

if __name__ == '__main__':
    # collect_addresses(cj, driver)
    apply_to_maps(cj, driver)
    driver.quit()
