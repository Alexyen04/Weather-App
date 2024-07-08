import tkinter as tk
from tkinter import ttk
import datetime as dt
import requests 

import window 

BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
API_KEY = "d274d311bcd15678b29f58537a8dfa4d"
CITY = "San Diego"

url = BASE_URL + "appid=" + API_KEY + "&q=" + CITY
response = requests.get(url).json()
#print(response)

def kelvinToCelciusAndFahrenheit(kelvin) :
    celsius = kelvin -273.15
    fahrenheit = (celsius * (9/5)) + 32
    return celsius, fahrenheit

def getData(): 
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

    #Windspeed
    windspeed = response['wind']['speed']

    #Time 
    timezoneDifference = response['timezone']
    currentTime = (dt.datetime.now(dt.timezone.utc) + dt.timedelta(seconds=timezoneDifference))
    naive_currentTime = currentTime.replace(tzinfo=None)
    print(naive_currentTime)

    #print(f"Temperature in {CITY}: {tempCelsius:.2f}°C or {tempFahrenheit:2f}°F")
    #print(f"Temperature in {CITY} feels like: {feelsLikeTempCelsius:.2f}°C or {feelsLikeTempFahrenheit:.2f}°F")


class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Weather App')
        self.root.geometry('500x750')

        self.input = tk.Text(self.root, height = 1, font = ('Arial', 15))
        self.input.pack(padx=10, pady=10)
        
        self.enterBtn = tk.Button(self.root, text= "Enter", font = ('Arial', 15), command=self.search)
        self.enterBtn.pack(padx=10, pady=10)

        self.root.mainloop()
    
    def search(self) :
        CITY = self.input.get('1.0', tk.END)
        print(CITY)

        url = BASE_URL + "appid=" + API_KEY + "&q=" + CITY
        response = requests.get(url).json()
        getData()
        #print(response)
        


GUI()



