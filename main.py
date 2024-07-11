import os
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import datetime as dt
from datetime import datetime

import requests 

BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
API_KEY = "d274d311bcd15678b29f58537a8dfa4d"
CITY = "Taipei"

def kelvinToCelciusAndFahrenheit(kelvin) :
    celsius = kelvin -273.15
    fahrenheit = (celsius * (9/5)) + 32
    return celsius, fahrenheit


url = BASE_URL + "appid=" + API_KEY + "&q=" + CITY
response = requests.get(url).json()
print(response)

#Actual Temperature
tempKelvin = response['main']['temp']
tempCelsius, tempFahrenheit = kelvinToCelciusAndFahrenheit(tempKelvin)

#Feels Like Temperature
feelsLikeTempKelvin = response['main']['feels_like']
feelsLikeTempCelsius, feelsLikeTempFahrenheit = kelvinToCelciusAndFahrenheit(feelsLikeTempKelvin)

#Temp Min
tempMinKelvin = response['main']['temp_min']
tempMinCelsius, tempMinFahrenheit = kelvinToCelciusAndFahrenheit(tempMinKelvin)

#Temp Max
tempMaxKelvin = response['main']['temp_max']
tempMaxCelsius, tempMaxFahrenheit = kelvinToCelciusAndFahrenheit(tempMaxKelvin)

#Pressure 
pressure = response['main']['pressure']

#Humidity
humidity = response['main']['humidity']

#Sea Level
seaLevel = response['main']['sea_level']

#Description
description = response['weather'][0]['description']
# list of all descriptions: scattered clouds, clear sky

#Clouds
clouds = response['clouds']['all']

#Windspeed
windspeed = response['wind']['speed']

#Time 
timezoneDifference = response['timezone']
currentTime = (dt.datetime.now(dt.timezone.utc) + dt.timedelta(seconds=timezoneDifference))
naive_currentTime = currentTime.replace(tzinfo=None)

sunsetTime = "20:00:00"
sunriseTime = "06:30:00"
datetime_format = "%H:%M:%S"
sunsetTime = datetime.strptime(sunsetTime, datetime_format)
sunriseTime = datetime.strptime(sunriseTime, datetime_format)
only_currentTime = datetime(1900, 1, 1, naive_currentTime.hour, naive_currentTime.minute, naive_currentTime.second)

# window
window = Tk()
window.title('Weather App')
window.geometry('500x750')

def set_background() :
    print(only_currentTime)
    if clouds > 50 :
        image_path = os.path.join(script_dir, "backgrounds", "rainybackground.jpg")
    elif (only_currentTime > sunsetTime) or (only_currentTime < sunriseTime):
        image_path = os.path.join(script_dir, "backgrounds", "Nightbackground.jpeg")
    else :     
        image_path = os.path.join(script_dir, "backgrounds", "Sunnybackground.jpg")

    return image_path

# background
# Get the directory of the current script
script_dir = os.path.dirname(__file__)

# Construct the relative path to the image file based on weather
image_path = set_background()

if not os.path.exists(image_path):
    print(f"Error: The file '{image_path}' does not exist.")
else:
    # background
    image = Image.open(image_path)
    resized_image = image.resize((525,775))
    sunny = ImageTk.PhotoImage(resized_image)
    label1 = Label(window, image=sunny)
    label1.place(x=-5, y=-5)

# run
window.mainloop()
