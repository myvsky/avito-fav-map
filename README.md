# Avito "Favorite" list map
## Display ads positions from Avito's "Favorite" list with Google Maps.

<img src="https://raw.githubusercontent.com/mayevskaya/mayevskaya/3087a0b60e0ba4b1bf9ad43e46ff3f64c086ddee/.src/rpg_cat.png" align=left width=8%>

[![Typing SVG](https://readme-typing-svg.demolab.com?font=Press+Start+2P&size=10&duration=1000&color=A08BD0&multiline=true&repeat=false&width=510&height=75&lines=This+is+the+first+Mayevskaya's+problem+in+production;programming.+The+microservice+outputs+positions;of+ads+from+Avito+Favorites+list.)](https://git.io/typing-svg)

### **_Approach_**
We use cookies from browser specified in `settings.ini`. 
You may use one of the following browsers for cookies retrieving:
|Name In Configuration|Full Name|
|-|-|-|
|chrome|Google Chrome|
|firefox|Mozilla Firefox|
|opera|Opera|
gx|Opera GX|
edge|Microsoft Edge
chromium|Chromium
brave|Brave
vivaldi|Vivaldi
safari|Safari

### **_Instructions_**
1. Log in to Avito in any browser that is specified in the list above.
2. Get Geocoder API key from Yandex.
3. Insert correct browser name (according to the table above) and API key to the corresponding
variables in `settings.ini`.
4. Launch main.py.

### Installation
```
git clone https://github.com/mayevskaya/avito-fav-map
cd avito-fav-map
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
```