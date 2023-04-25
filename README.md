# **Avito Favorites Map**
## _Display ads positions from Avito Favorites on Yandex Maps with Geocoder API_
---
## **Description**
We use cookies from browser specified in `settings.ini`. 
You may use one of the following browsers for cookies retrieving:
|Preferred Browser|What You Past In `settings.ini`
|-|-|
Google Chrome|chrome|
Mozilla Firefox|firefox|
|Opera|opera
|Opera GX|gx
Microsoft Edge|edge|
|Chromium|chromium
|Brave|brave|
|Vivaldi|vivaldi|
|Safari|safari|

After using the microservice once, you can access the received map anytime at path: `{path_to_avito-fav-map}/renderedMap.html`.

## **Instructions**
### 1. Log in to Avito in preferred browser (available browsers specified in the table above)
### 2. [Get Yandex Geocoder API key](https://developer.tech.yandex.ru/services) (Connect API -> JavaScript and Geocoder API)
### 3. Insert preferred browser name (step 1) and API key (step 2) to the corresponding variables in `settings.ini`
### 4. Launch main.py

## **Installation**
```
git clone https://github.com/mayevskaya/avito-fav-map
cd avito-fav-map
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
```