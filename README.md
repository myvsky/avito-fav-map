# Avito favorites map
## Display ads positions from Avito's Favorite list with Google Maps.
### Description
The microservice uses Chrome cookies to gain access to the Avito account
without the need for authorization each time it is used. Read the instruction
below to find out capabilities of microservice.

### Installation:
```
git clone https://github.com/mayevskaya/avito-fav-map
cd avito-fav-map
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
```
### Instructions:
1. Log in to Avito with your default browser.
2. Launch main.py, give permission for "browsercookie" library to use Chrome
browser cookies.
3. After successful gaining data.csv file, redirect to the following page:
https://google.com/maps/d/u/0 and create new map.
4. In layers list, import data from data.csv file.
