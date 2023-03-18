# Avito favorites map
## Display ads positions from Avito's Favorite list with Google Maps.
### Description
The microservice uses Chrome cookies to gain access to the Avito and Google Maps
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
3. Launch main.py, give permission for "browsercookie" library to use Chrome
browser cookies.
As it was mentioned in description, all you need for successful running of
microservice is having up-to-date cookies of your accounts. From the server
side, it will seem like you're not using any automated software to access 
and use data.

### Additions

• If you have multiple Google Accounts, you can switch between them by editing
url in the apply_to_maps function.
• If you'd like to use any other than Chrome browser, you must refactor the
code according to your needs.
• This repository was tested on Unix system (Mac OS). If you are getting exceptions
in code using any other system, it was expected. We offer the user to modify the 
code to suit the features of their operating system as a simple exercise.
