import os
import ssl
import requests
import urllib.parse
import browser_cookie3

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util import ssl_
from bs4 import BeautifulSoup


# Get cookiejar
def get_cj() -> dict: 

    # Check the cache file on existance and accuracy
    def create_cache():
        print("""What browser stores your Avito account info? Choose an option:
        |N| Name     | Supported OS
        |-|----------|--------------------
        [1] Chrome   | Linux, OSX, Windows
        [2] Firefox  | Linux, OSX, Windows
        [3] Opera    | Linux, OSX, Windows
        [4] Opera GX | OSX, Windows
        [5] Edge     | Linux, OSX, Windows
        [6] Chromium | Linux, OSX, Windows
        [7] Brave    | Linux, OSX, Windows
        [8] Vivaldi  | Linux, OSX, Windows
        [9] Safari   | OSX
        ----------------------------------""")
        option = input("\n\nOption number: ")
        while option not in set("123456789"):
            option = input("Incorrect option number. Try again: ")
        match option:
            case '1': browser = "Chrome"
            case '2': browser = "Firefox"
            case '3': browser = "Opera"
            case '4': browser = "GX"
            case '5': browser = "Edge"
            case '6': browser = "Chromium"
            case '7': browser = "Brave"
            case '8': browser = "Vivaldi"
            case '9': browser = "Safari"

        print(f"""All done! Cookies exported. {browser} is set as default browser for Avito cookie export.
        You can change it anytime by deleting `browser_cached.txt` from current working directory.""")
        open("browser_cached.txt", "w", encoding="utf-8").write(browser)

    if (not os.path.exists("browser_cached.txt")) or (len(open("browser_cached.txt", "r").read().split()) != 1) or (
        open("browser_cached.txt", "r").read().strip() not in [
            "Chrome", "Firefox", "Opera", "GX", "Edge", "Chromium", "Brave", "Vivaldi", "Safari"]):
            create_cache()

    # Regular cookie jar picking
    browser = open("browser_cached.txt", "r").read()
    match browser:
        case "Chrome": cj = browser_cookie3.chrome()
        case "Firefox": cj = browser_cookie3.firefox()
        case "Opera": cj = browser_cookie3.opera()
        case "GX": cj = browser_cookie3.opera_gx()
        case "Edge": cj = browser_cookie3.edge()
        case "Chromium": cj = browser_cookie3.chromium()
        case "Brave": cj = browser_cookie3.brave()
        case "Vivaldi": cj = browser_cookie3.vivaldi()
        case "Safari": cj = browser_cookie3.safari()

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
    
    # Get all addresses using regular expression
    adrs = soup.find_all(lambda x: x.has_attr('class') and "location-addressLine" in ''.join(x['class']))
    # Get all the names using regular expression
    names = soup.find_all(lambda x: x.has_attr('class') and x.name == "strong" and "styles-module" in ''.join(x['class']))
    # Get all the links using regular expression
    links = soup.find_all(lambda x: x.has_attr('class') and x.name == "a" and "css" in ''.join(x['class']))
    
    # Convert result to lists
    return [a.text for a in adrs], [n.text for n in names], ["https://avito.ru" + a['href'] for a in links]


if __name__ == "__main__":
    print(parse_page())