# Avito favorites map
## Display ads positions from Avito's Favorite list with Google Maps.
### Description
The microservice uses Chrome cookies to gain access to the Avito and Google Maps
accounts without the need for authorization each time it is used.

### Installation:
```
git clone https://github.com/mayevskaya/avito-fav-map
cd avito-fav-map
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
```

### Instructions
1. Log in to Avito and Google Maps with Chrome browser.
2. Launch main.py, give permission for "browsercookie" library to use Chrome
browser cookies.
3. After successful gaining data.csv file, redirect to the following page:
https://google.com/maps/d/u/0 and create new map.
4. In layers list, import data from data.csv file.

### Recommendations

1. If you have multiple Google Accounts and don't want to use the default (0)
one, you must change url in the apply_to_maps function according to comments
above the variable.
2. If you'd like to use any other than Chrome browser, you must refactor the
code according to your needs.
