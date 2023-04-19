import ssl
import requests
import urllib.parse
import browser_cookie3

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util import ssl_
from bs4 import BeautifulSoup


# Get cookiejar
def get_cj() -> dict: 
    print("""What browser stores your Avito account info? Choose an option:
[1] - Chrome
[2] - Firefox
[3] - Safari""")
    pass



# Get contents of page
def get_page() -> str:

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
    encoded_response = session.request('GET', 'https://www.avito.ru/favorites').text

    # Instantly decode it and return the result
    return urllib.parse.unquote(encoded_response)


# Parse addresses, names and links of ads
def parse_page(html=get_page()):
    # Parse document
    soup = BeautifulSoup(html, 'html.parser')
    
    # Get all addresses using regular expression (lambda function)
    adrs = soup.find_all(lambda x: "location-addressLine" in x)
    
    # Convert result to dictionary