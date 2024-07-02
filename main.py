import datetime as dt
import requests 

BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
CITY = "San Diego"

url = BASE_URL + "appid=" + "251e61a1560524440fb982133cbce2da" + "&q=" + CITY

reponse = requests.get(url).json()

print(reponse)