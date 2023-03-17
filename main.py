import csv
import browsercookie
import os
import time
import webbrowser
from selenium import webdriver
from selenium.webdriver.common.by import By

# Gain cookies from Chrome browser
cj = browsercookie.chrome()

# Use 'headless' Chrome as a webdriver
driver = webdriver.Chrome()

# Collect needed data from Avito.ru
def collect_addresses(cj, driver):

    print("Connecting to your Avito account...")
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

    print("Successfully! Exporting the address lines of your Favorite ads...")
    # Find all the addresses
    adrs = driver.find_elements(By.CLASS_NAME, "location-addressLine-fHEor")

    # Convert webobjects to the list
    adrs = [i.text for i in elements]

    # List must not be empty
    if len(adrs) != 0:
        with open("data.csv", mode="w", encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Адреса"])
            for adr in adrs:
                writer.writerow([element])
    else:
        raise Exception("You're not logged in Avito or your Favorite list is empty")

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
        if cookie.domain == ".google.com":
            driver.add_cookie(({
                'name': cookie.name,
                'value': cookie.value,
                'domain': cookie.domain,
                'path': cookie.path,
                'expires': cookie.expires
        }))

    # Apply cookies
    driver.get(url)

    # Click on the "Create new map" button
    button = driver.find_element(By.XPATH, '//*[@id="docs-editor"]/div[2]/div[2]/div[1]/div[1]/div/span/span')
    button.click()
    driver.implicitly_wait(10)

    print("Successfully! Creating new map which contains exported addresses")

    # Open import overlay
    button = driver.find_element(By.XPATH, '//*[@id="ly0-layerview-import-link"]')
    button.click()
    driver.implicitly_wait(10)

    # Switch to overlay to navigate in its elements
    picker = driver.find_element(By.CLASS_NAME, 'picker-dialog-content')
    iframe = picker.find_element(By.TAG_NAME, 'iframe')
    driver.switch_to.frame(iframe)
    driver.implicitly_wait(10)

    # Find the import button, make it an input and feed a file to it
    target = driver.find_element(By.XPATH, '//*[@id=":n"]/div')
    JS_DROP_FILE="    var target = arguments[0],        offsetX = arguments[1],        offsetY = arguments[2],        document = target.ownerDocument || document,        window = document.defaultView || window;    var input = document.createElement('INPUT');    input.type = 'file';    input.onchange = function () {      var rect = target.getBoundingClientRect(),          x = rect.left + (offsetX || (rect.width >> 1)),          y = rect.top + (offsetY || (rect.height >> 1)),          dataTransfer = { files: this.files };      ['dragenter', 'dragover', 'drop'].forEach(function (name) {        var evt = document.createEvent('MouseEvent');        evt.initMouseEvent(name, !0, !0, window, 0, 0, 0, x, y, !1, !1, !1, !1, 0, null);        evt.dataTransfer = dataTransfer;        target.dispatchEvent(evt);      });      setTimeout(function () { document.body.removeChild(input); }, 25);    };    document.body.appendChild(input);    return input;"
    parent = target.parent
    file_input = parent.execute_script(JS_DROP_FILE, target, 0, 0)
    file_input.send_keys(os.path.join(os.getcwd(), 'data.csv'))
    driver.implicitly_wait(10)

    # Confirm and apply addresses to the new map
    driver.switch_to.default_content()
    button = driver.find_element(By.ID, "upload-checkbox-0")
    button.click()
    driver.implicitly_wait(10)
    button = driver.find_element(By.NAME, "location_step_ok")
    button.click()
    driver.implicitly_wait(10)
    button = driver.find_element(By.ID, "upload-radio-0")
    button.click()
    driver.implicitly_wait(10)
    button = driver.find_element(By.NAME, "name_step_ok")
    button.click()
    print("All done! Saving the result to your account...") 
    print("You'll be redirected to the Google Maps page in 10 seconds")
    # Wait ten seconds until the page is loaded and saved
    time.sleep(10)
    webbrowser.open(url)

    

if __name__ == '__main__':
    try:
        collect_addresses(cj, driver)
    except:
        print("Something went wrong while collecting addresses from Avito. Check your internet connection")
    try:
        apply_to_maps(cj, driver)
    except:
        print("Something went wrong while importing data.csv to Google Maps. Check your internet connection and if you are logged in")
    driver.quit()