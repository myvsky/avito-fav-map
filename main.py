import csv
import browser_cookie3
import os
import time
import webbrowser
from datetime import datetime
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By


# Confirmation
print("""\nBy proceeding you agree with microservice's policy:
* Will use your Chrome's browser cookies
* You must be logged into Google Maps and Avito accounts
* You will not abuse the traffic, otherwise your IP will be blocked by Avito\n\n""")

# Gain cookies from Chrome browser
cj = browser_cookie3.chrome()

# Use 'headless' Chrome as a webdriver
options = Options()
options.add_argument('window-size=1366x768')
options.add_argument('--start-maximized')
options.add_argument('--headless')
driver = webdriver.Chrome(options=options, executable_path="chromedriver")

# Collect needed data from Avito.ru
def collect_addresses(cj, driver):

    print("Connecting to your Avito account...")
    url = "https://avito.ru/favorites"
    driver.get(url)
    # Apply only cookies with Avito's domain
    print("Applying cookies and refreshing the page...")
    for cookie in cj:
        if ".avito.ru" in cookie.domain:
            driver.add_cookie({
                "name": cookie.name,
                "value": cookie.value
        })

    # Apply cookies with forced page refresh
    driver.get(url)
    print("Successfully! Exporting the address lines of your Favorite ads...\n")

    # Find address elements
    adrs = driver.find_elements(By.XPATH, "//*[contains(@class, 'location-addressLine')]")

    # Adrs list must not be empty
    if not adrs:
        # Suggest for authorization in browser and forced microservice stopping
        webbrowser.open(url)
        raise Exception("It seems like we haven't found any items in your list. Maybe the list is empty or you're not logged in?")
    while len(adrs) % 20 == 0:
        print("We've reached page limit = 20 ads per page. Load more ads?\n")
        ans = input("y/n: ")
        while ans.lower() not in ["y", "n"]:
            continue
        if ans == 'n':
            break
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Load more ad elements
        adrs = driver.find_elements(By.XPATH, "//span[contains(@class, 'location-addressLine')]")

    hrefs = driver.find_elements(By.XPATH, "//div[contains(@class, 'item-snippet-column-2')]/a")
    # Pair each href and adr
    adr_and_href = [[adr.text, href.get_attribute('href')] for adr, href in zip(adrs, hrefs)]

    with open("data.csv", mode="w", encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        # Header row containing two columns
        writer.writerow(["Addresses", "Links"])
        # Export unique text instead of web object
        for i, (adr,link) in enumerate(adr_and_href):
            writer.writerow([adr, link])

    print("CSV file appeared in current directory")


def apply_to_maps(cj, driver):

    # Load page and cookies
    # url : Google Maps of concrete user
    # If you have multiple accounts, you need to change the last symbol of the
    # variable to the number of corresponding account
    print("Connecting to your Google Maps account...")
    url = "https://google.com/maps/d/u/0"
    driver.get(url)

    for cookie in cj:
        if ".google.com" == cookie.domain:
            driver.add_cookie(({
                'name': cookie.name,
                'value': cookie.value,
                'domain': cookie.domain
        }))

    # Apply cookies
    driver.get(url)
    print("Connected to account accroding to your cookies. Creaing new map...")
    # Click on the "Create new map" button
    try:
        button = driver.find_element(By.XPATH, '//*[@id="docs-editor"]/div[2]/div[2]/div[1]/div[1]/div')
        button.click()
        driver.implicitly_wait(10)

        # Rename the map
        button = driver.find_element(By.XPATH, '//*[@id="map-title-desc-bar"]/div[1]')
        button.click()
        driver.implicitly_wait(10)
        inp = driver.find_element(By.XPATH, '//*[@id="update-map"]//div//input')
        inp.send_keys(f'Avito Favorite {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        # Confirm
        button = driver.find_element(By.XPATH, '//*[@id="update-map"]/div[3]/button[1]')
        button.click()
        driver.implicitly_wait(10)

        # Open import overlay
        button = driver.find_element(By.XPATH, '//*[@id="ly0-layerview-import-link"]')
        button.click()
        driver.implicitly_wait(10)

        # Switch to overlay to navigate in its elements
        picker = driver.find_element(By.CLASS_NAME, 'picker-dialog-content')
        iframe = picker.find_element(By.TAG_NAME, 'iframe')
        driver.switch_to.frame(iframe)
        driver.implicitly_wait(10)

        # Feed file into the input field
        target = driver.find_element(By.XPATH, "//input[contains(@accept, '.CSV')]")
        target.send_keys(os.path.join(os.getcwd(), 'data.csv'))
        driver.implicitly_wait(10)

        # Confirm and apply addresses to the new map
        driver.switch_to.default_content()
        button = driver.find_element(By.ID, "upload-checkbox-0")
        button.click()
        driver.implicitly_wait(10)
        button = driver.find_element(By.NAME, "location_step_ok")
        button.click()
        driver.implicitly_wait(10)
        button = driver.find_element(By.ID, "upload-radio-1")
        button.click()
        driver.implicitly_wait(10)
        button = driver.find_element(By.NAME, "name_step_ok")
        button.click()
        print("All done! Saving the result to your account...") 
        print("You'll be redirected to the Google Maps page in 5 seconds")
        # Wait 5 seconds until the page is loaded and saved
        time.sleep(5)
        url = driver.current_url
        webbrowser.open(url)
    except:
        webbrowser.open(driver.current_url)
        print("""It seems like you're not logged in to Google Maps account.
Log in to your account in Chrome browser and come back.""")

    

if __name__ == '__main__':
    collect_addresses(cj, driver)
    apply_to_maps(cj, driver)
    driver.quit()