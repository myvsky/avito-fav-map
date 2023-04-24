# For applying and displaying ads' positions
import requests
import webbrowser

# For `settings.ini`
import os
import configparser

# For requesting Avito page 
import browser_cookie3
from playwright.sync_api import sync_playwright
import time     # Time delay for loading DOM content

# For parsing ads' names, links and positions
from bs4 import BeautifulSoup


print("Setting configuration from `settings.ini`...")
# Get configuration from settings
config = configparser.ConfigParser()
config.read('settings.ini')

browser = config.get('general', 'browser')
API_key = config.get('general', 'API_key')
print("Done!\n")


# Get cookiejar
def get_cj() -> dict: 

    # Regular cookie jar picking
    match browser.lower():
        case "chrome": cj = browser_cookie3.chrome()
        case "firefox": cj = browser_cookie3.firefox()
        case "opera": cj = browser_cookie3.opera()
        case "gx": cj = browser_cookie3.opera_gx()
        case "edge": cj = browser_cookie3.edge()
        case "chromium": cj = browser_cookie3.chromium()
        case "brave": cj = browser_cookie3.brave()
        case "vivaldi": cj = browser_cookie3.vivaldi()
        case "safari": cj = browser_cookie3.safari()
        case _: raise Exception("Wrong browser name found in `settings.ini`. Killing the task...")

    print("Retrieving cookies from browser pointed in `settings.ini`...\n")
    # Convert cookiejar in the right form
    cj = [
        {
        "name": cookie.name,
        "value": cookie.value,
        "domain": cookie.domain,
        "path": cookie.path
        }
        for cookie in cj
        # Extract only Avito-relatable cookies
        if ".avito.ru" in cookie.domain
    ]

    print("Done!\n")
    return cj


# Get contents of page
def parse_page(cj=get_cj()) -> list:

    print("Launching Chromium webdriver, loading Avito Favorites page...")
    # Launch Chromium webdriver
    with sync_playwright() as p:
        browser = p.chromium.launch()

        # Create context for cookie uploading
        ctx = browser.new_context()
        ctx.add_cookies(cj)

        # Load Avito Favorites page
        page = ctx.new_page()
        page.goto('https://avito.ru/favorites')

        print("Collecting all ads from Favorites...")
        # Look how many ads we have at current state
        while 1:
            # Check page content
            html = page.content()
            # Create soup object to track when we are done with loading all the ads
            soup = BeautifulSoup(html, 'html.parser')
            ads = soup.find_all(lambda x: x.has_attr('class') and "item-snippet-root" in ''.join(x['class']))

            # If no more ads to be loaded, exit the loop
            if len(ads) % 20 != 0: break

            # Else keep retrieving ads information
            # Scroll down
            page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
            # Time delay for more ads to load
            time.sleep(0.5)

        browser.close()

    print("Sorting addresses, name, links from each ad...")
    data = []
    for ad in ads:
        # To avoid absence of links, check it on NoneType
        adr = ad.find(lambda x: x.has_attr('class') and 'location-addressLine' in ''.join(x['class']))
        if not adr: continue
        else: adr = adr.text
        name = ad.find(lambda x: x.has_attr('class') and x.name == "strong" and 'styles-module' in ''.join(x['class']))
        if not name: continue
        else: name = name.text
        link = ad.find(lambda x: x.has_attr('class') and x.name == 'a' and 'css' in ''.join(x['class']))
        if not link: continue
        else: link = f"https://avito.ru{link['href']}"

        # Connect each data with each other
        data.append([
            adr,
            name,
            link
            ])

    print("Done!\n")
    return data

def get_content_table(data) -> str:
    print("Creating table of contents for the map...")
    response = "<table><th>ID</th><th>Ad Name+Link</th><th>Address</th>"
    addresses = [k[0] for k in data]
    names = [k[1] for k in data]
    links = [k[2] for k in data]
    for i in range(len(addresses)):
        response+=f"<tr><td>{i}</td><td><a href={links[i]}>{names[i]}</a></td><td id='table-address-{i}'>{addresses[i]}</td></tr>"

    print("Done!\n")
    return response


def get_address_coords(data) -> str:

    print("Creating scripts for displaying positions on the map...")
    # Sort information from list
    addresses = [k[0] for k in data]
    names = [k[1] for k in data]
    links = [k[2] for k in data]
    placemark_js = ""
    for i in range(len(addresses)):
        geocode_url = f"https://geocode-maps.yandex.ru/1.x/?apikey={API_key}&format=json&geocode={addresses[i]}"
        try:
            response = requests.get(geocode_url).json()
            coords = response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]
            lat, lon = coords.split()[::-1]
            placemark_js += f'''
                var placemark = new ymaps.Placemark([{lat}, {lon}], {{
                    hintContent: "{names[i].title().replace('"', "'")}",
                    balloonContent: "{links[i]}"
                }});
                myMap.geoObjects.add(placemark);
                var tableRow = document.getElementById('table-address-{i}');

                tableRow.addEventListener('click', function (event) {{
                myMap.setCenter([{lat}, {lon}], 15);
                }});
            '''
        except KeyError:
            raise ValueError(f"Failed to retrieve coordinates for ad (name: {names[i]}, address: {addresses[i]}, link: {links[i]}) from Yandex Geocoder API.")

    print("Done!\n")
    return placemark_js


def map_renderer(data) -> str:

    print("Creating HTML document...")
    # Create HTML content
    html_content = f'''
    <!DOCTYPE html><html lang=en><head><title>Avito Favorites Map</title>
        <script src="https://api-maps.yandex.ru/2.1/?lang=ru_RU" type="text/javascript"></script>
        <script>
        ymaps.ready(init);function init() {{var myMap = new ymaps.Map("map", {{center: [55.76, 37.64], zoom: 5}});
                {get_address_coords(data=data)}
                }}
        </script><style>#map{{width:70%;height:97vh;position:absolute;right:10px;}}#desc{{width:28%;height:97vh;}}</style></head>
        <body><div id=map></div><div id=desc>{get_content_table(data=data)}</div></html>
    '''

    # Save the HTML content to a file
    open('renderedMap.html', 'w').write(html_content)

    print("""renderedMap.html file has been created. You can access it in current work directory anytime.\n
             -------
\nAll done. Finishing the process.""")


if __name__ == "__main__":
    print("Applying data to the map...")
    map_renderer(data=parse_page())
    webbrowser.open(f"file://{os.getcwd()}/renderedMap.html")
    print("All done! You can check the resulting work in `map.html` anytime.")