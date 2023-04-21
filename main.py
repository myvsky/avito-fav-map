import webbrowser
import os
import configparser
import ssl
import requests
import urllib.parse
import browser_cookie3

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util import ssl_
from bs4 import BeautifulSoup


# Get info from
config = configparser.ConfigParser()
config.read('settings.ini')

browser = config.get('general', 'browser')
API_key = config.get('general', 'API_key')

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

    return cj


# Get contents of page
def get_page(cj=get_cj()) -> str:

    # Ciphers for encoding/decoding sensitive data that Avito use
    CIPHERS = """ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-SHA256:AES256-SHA"""

    # Define SSL/TLS options
    ssl_options = ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1

    # Create a requests session
    session = requests.session()

    # Create a custom SSL context using ssl_.create_urllib3_context
    ctx = ssl_.create_urllib3_context(ciphers=CIPHERS, cert_reqs=ssl.CERT_REQUIRED, options=ssl_options)

    # Mount the custom SSL context to the session for HTTPS requests
    adapter = HTTPAdapter(pool_maxsize=10, max_retries=3)
    adapter.init_poolmanager(connections=10, maxsize=10, ssl_context=ctx)
    session.mount("https://", adapter)

    # Get a URL-encoded string
    encoded_response = session.request('GET', 'https://www.avito.ru/favorites', cookies=cj)

    # Instantly decode it and return the result
    return urllib.parse.unquote(encoded_response.text)


# Parse addresses, names and links of ads
def parse_page(html=get_page()) -> list:
    # Parse document
    soup = BeautifulSoup(html, 'html.parser')
    
    # Get all the ads
    ads = soup.find_all(lambda x: x.has_attr('class') and "item-snippet-root" in ''.join(x['class']))

    data = []
    for ad in ads:
        # To avoid absence of links, check it on NoneType
        adr = ad.find(lambda x: x.has_attr('class') and 'location-addressLine' in ''.join(x['class']))
        adr = None if not adr else adr.text
        name = ad.find(lambda x: x.has_attr('class') and x.name == "strong" and 'styles-module' in ''.join(x['class']))
        name = None if not name else name.text
        link = ad.find(lambda x: x.has_attr('class') and x.name == 'a' and 'css' in ''.join(x['class']))
        link = None if not link else f"https://avito.ru{link['href']}"

        # Connect each data with each other
        data.append([
            adr,
            name,
            link
            ])

    return data


import requests

def display_addresses_on_map() -> str:
    # Create the HTML content
    html_content = f'''
    <!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Avito Favorites Map</title>
        <script src="https://api-maps.yandex.ru/2.1/?lang=en_US" type="text/javascript"></script>
        <script>
            ymaps.ready(init);
            function init() {{
                var myMap = new ymaps.Map("map", {{
                    center: [55.76, 37.64], // Set the initial center of the map
                    zoom: 10 // Set the initial zoom level of the map
                }});

                // Iterate over the addresses and create placemarks for each address
                {get_address_coords()}

            }}
        </script>
        <style>body{{color:aliceblue;background-color:rgb(45,45,50);margin:0;}}#map{{width:70%;height:100%;position:absolute;right:0;}}#desc{{width:30%;height:max-content;}}</style>
    </head>
    <body><div id="map"></div><div id="desc">{get_text_info()}</div></body></html>
    '''

    # Save the HTML content to a file
    open('renderedMap.html', 'w').write(html_content)

    print('renderedMap.html file has been created. You can access it in current work directory anytime.')


def get_text_info(data=parse_page()) -> str:
    response = "Name\t\t\tAddress"
    addresses = [k[0] for k in data]
    names = [k[1] for k in data]
    links = [k[2] for k in data]
    for i in range(len(addresses)):
        response+=f"<p><a href={links[i]}>{names[i]}</a>\t\t{addresses[i]}</p>"

    return response

def get_address_coords(data=parse_page()) -> str:

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
                    hintContent: '{names[i].title()}',
                    balloonContent: '{links[i]}'
                }});
                myMap.geoObjects.add(placemark);
            '''
        except KeyError:
            raise ValueError(f"Failed to retrieve coordinates for ad (name: {names[i]}, address: {addresses[i]}, link: {links[i]} from Yandex Geocoder API.")

    return placemark_js



if __name__ == "__main__":
    print("Applying data to the map...")
    display_addresses_on_map()
    webbrowser.open(f"file://{os.getcwd()}/renderedMap.html")
    print("All done! You can check the resulting work in `map.html` anytime.")