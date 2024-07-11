import os
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import datetime as dt
from datetime import datetime

import requests 

BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
API_KEY = "d274d311bcd15678b29f58537a8dfa4d"
CITY = "San Diego"
tempFahrenheit = None
tempCelcius = None
feelsLikeTempFahrenheit = None 
feelsLikeTempCelsius = None
tempMinCelsius = None
tempMinFahrenheit = None
tempMaxCelsius = None
tempMaxFahrenheit = None
pressure = None
humidity = None
seaLevel = None
deascription = None
windSpeed = None

def kelvinToCelciusAndFahrenheit(kelvin) :
    celsius = kelvin -273.15
    fahrenheit = (celsius * (9/5)) + 32
    return celsius, fahrenheit

def setData(city): 
    global tempFahrenheit, tempCelsius, feelsLikeTempFahrenheit, feelsLikeTempCelsius
    global pressure, humidity, seaLevel, description, windSpeed

    url = BASE_URL + "appid=" + API_KEY + "&q=" + city
    response = requests.get(url).json()

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
    windSpeed = response['wind']['speed']

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

def search():
    global CITY
    CITY = input.get('1.0', tk.END)
    setData(CITY)

    url = BASE_URL + "appid=" + API_KEY + "&q=" + CITY
    response = requests.get(url).json()

    #labels
    temp = tk.Label(root, text= f"Temperature: {tempFahrenheit:.2f}°F", background= 'pink')
    feelsTemp = tk.Label(root, text= f"Feels Like Temperature: {feelsLikeTempFahrenheit:.2f}°F", background= 'pink')
    pressureLabel = tk.Label(root, text= f"Pressure: {pressure}", background= 'pink')
    humidityLabel = tk.Label(root, text= f"Humidity: {humidity}", background= 'pink')
    seaLevelLabel = tk.Label(root, text= f"Sea Level: {seaLevel}", background= 'pink')
    descriptionLabel = tk.Label(root, text= f"Description: {description}", background= 'pink')
    windSpeedLabel = tk.Label(root, text= f"WindSpeed: {windSpeed}", background= 'pink')

    #grid
    temp.grid(row= 1, columnspan= 2, sticky= 'nsew')
    feelsTemp.grid(row= 2, columnspan= 2, sticky= 'nsew')
    pressureLabel.grid(row= 3, columnspan= 2, sticky= 'nsew')
    humidityLabel.grid(row= 4, columnspan= 2, sticky= 'nsew')
    seaLevelLabel.grid(row= 5, columnspan= 2, sticky= 'nsew')
    descriptionLabel.grid(row= 6, columnspan= 2, sticky= 'nsew')
    windSpeedLabel.grid(row= 7, columnspan= 2, sticky= 'nsew')

    print(response)

def set_background() :
    print(only_currentTime)
    if clouds > 50 :
        image_path = os.path.join(script_dir, "backgrounds", "rainybackground.jpg")
    elif (only_currentTime > sunsetTime) or (only_currentTime < sunriseTime):
        image_path = os.path.join(script_dir, "backgrounds", "Nightbackground.jpeg")
    else :     
        image_path = os.path.join(script_dir, "backgrounds", "Sunnybackground.jpg")

    return image_path
    
#Window 
root = tk.Tk()
root.title('Weather App')
root.geometry('500x750')

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
    background_image = ImageTk.PhotoImage(resized_image)
    label1 = Label(root, image=background_image)
    label1.place(x=-5, y=-5)

#input
input = tk.Text(root, height = 1, font = ('Arial', 15), background= 'pink')

#button
enterBtn = tk.Button(root, text= "Enter", font = ('Arial', 15), command=search)
        
#grid
root.columnconfigure(0, weight= 3, uniform= 'a')
root.columnconfigure(1, weight= 1, uniform= 'a')

root.rowconfigure((0,1,2,3,4,5,6,7), weight= 1, uniform= 'a')

input.grid(row= 0, column= 0, sticky= 'nsew')
enterBtn.grid(row= 0, column= 1, sticky= 'nsew')

root.mainloop()
