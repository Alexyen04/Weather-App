import datetime as dt
import requests 

BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
API_KEY = "d274d311bcd15678b29f58537a8dfa4d"
CITY = "San Diego"

url = BASE_URL + "appid=" + API_KEY + "&q=" + CITY

response = requests.get(url).json()

print(response)

