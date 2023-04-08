# Avito "Favorite" list map
## Display ads positions from Avito's "Favorite" list with Google Maps.

<img src="https://raw.githubusercontent.com/mayevskaya/mayevskaya/3087a0b60e0ba4b1bf9ad43e46ff3f64c086ddee/.src/rpg_cat.png" align=left width=8%>

[![Typing SVG](https://readme-typing-svg.demolab.com?font=Press+Start+2P&size=9&duration=4550&color=A08BD0&multiline=true&repeat=false&width=720&height=75&lines=Hi!+This+is+the+first+Mayevskaya's+intershipment+problem.+The+purpose+is+making+a;microservice+for+displaying+ads+from+Avito+"Favorite"+list+in+the+visual+way,+on;the+Google+Maps+in+particular.+There+are+no+API+usage,+pure+parsing+with+Python.;Find+more+details+and+approach+below.)](https://git.io/typing-svg)
<details>
<summary>TL;DR</summary>
This is my first intershipment problem I've ever solved. The purpose of this project is visual interpreting ads from Avito "Favorite" list. In particular, the position of each ad was displayed on the Google Maps. No API usage, only pure parsing with Python. 
</details>

### Approach
The microservice use Chrome cookies to gain access to the Avito and Google Maps
accounts without the need for authorization each time it is used. Need to keep
log in to accounts of both services. Cookies must be up-to-date.

### Installation
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