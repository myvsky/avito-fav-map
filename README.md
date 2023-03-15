# Avito favorites map
## Display your favorite items from Avito.ru on the Google Maps.
---
### Installation:
```
git clone https://github.com/mayevskaya/avito-fav-map
cd avito-fav-map
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
```
### Requirements:
- You are logged in with Avito;
- You accept Avito's cookies usage;
- You give permission for "browsercookie" module to use your "physical
browser" cookies for webdriver to get into your account without needing to get
through manual authorization every time;

### Remarks and explainations:
This repository lets you to get all the addresses from your "Favorite" list on
Avito. Those addresses will be stored in .csv file, which you can use to 
display all those marks of addresses on the Google Maps.

### Displaying addresses via Google Maps:
1. Redirect to the following website: https://google.com/maps/d/u/0;
2. Click on the "CREATE NEW MAP" button OR use the one that exists already
(if you want to);
3. Click "Add layer" and choose the "Import" button in panel of appended
layer.
