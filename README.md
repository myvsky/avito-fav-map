# Avito map of Favorites list
## Display ads positions from Favorites list with Google Maps.
### Description
The microservice use Chrome cookies to gain access to the Avito and Google Maps
accounts without the need for authorization each time it is used. Need to keep
log in to accounts of both services. Cookies must be up-to-date.

### Installation:
```
git clone https://github.com/mayevskaya/avito-fav-map
cd avito-fav-map
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
```

### Instructions
1. Log in to Avito account with Chrome browser.
2. Log in to Google Maps account with Chrome browser.
3. Launch main.py, give permission for "browser_cookie3" library to use Chrome (if needed)

### Additions

• If you have multiple Google Accounts, you can switch between them by editing
url in the apply_to_maps function.
• Google Maps complying on data incorrections from N rows is not the problem of the code, it's Google Maps bug.