import tkinter as tk
from tkinter import ttk
import datetime as dt
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
    global tempFahrenheit, tempCelsius, feelsLikeTempFahrenheit, feelsLikeTempCelsius, tempMinCelsius, tempMinFahrenheit, tempMaxCelsius, tempMaxFahrenheit
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

    #Windspeed
    windSpeed = response['wind']['speed']

    #Time 
    timezoneDifference = response['timezone']
    currentTime = (dt.datetime.now(dt.timezone.utc) + dt.timedelta(seconds=timezoneDifference))
    naive_currentTime = currentTime.replace(tzinfo=None)

    #print(naive_currentTime)
    #print(f"Temperature in {CITY}: {tempCelsius:.2f}C or {tempFahrenheit:2f}F")
    #print(f"Temperature in {CITY} feels like: {feelsLikeTempCelsius:.2f}C or {feelsLikeTempFahrenheit:.2f}F")

def search(event=None):
    global CITY
    CITY = input.get()
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
    lowTempLabel = tk.Label(root, text= f"Low: {tempMinFahrenheit:.2f}°F", background= 'pink')
    highTempLabel = tk.Label(root, text= f"High: {tempMaxFahrenheit:.2f}°F", background= 'pink')

    #grid
    temp.grid(row= 1, columnspan= 2, sticky= 'nsew')
    feelsTemp.grid(row= 2, columnspan= 2, sticky= 'sew')
    lowTempLabel.grid(row= 3, column= 0, sticky= 'nse')
    highTempLabel.grid(row= 3, column= 1, sticky= 'nsw')   
    descriptionLabel.grid(row= 4, columnspan= 2, sticky= 'new')

    pressureLabel.grid(row= 5, column= 0, sticky= 'nsew')
    humidityLabel.grid(row= 5, column= 1, sticky= 'nsew')
    seaLevelLabel.grid(row= 6, column= 0, sticky= 'nsew')
    windSpeedLabel.grid(row= 6, column= 1, sticky= 'nsew')

    print(response)

def bind_enter(event):
    root.bind('<Return>', search)

def unbind_enter(event):
    root.unbind('<Return>')

#Window 
root = tk.Tk()
root.title('Weather App')
root.geometry('500x750')

#input
input = tk.Entry(root, font = ('Arial', 15), background= 'lightblue')


# Bind focus in and out events
input.bind('<FocusIn>', bind_enter)
input.bind('<FocusOut>', unbind_enter)
        
#grid
root.columnconfigure(0, weight= 1, uniform= 'a')
root.columnconfigure(1, weight= 1, uniform= 'a')

root.rowconfigure(0, weight= 1, uniform= 'a')
root.rowconfigure(1, weight= 6, uniform= 'a')
root.rowconfigure((2,3,4), weight= 2, uniform= 'a')
root.rowconfigure((5,6), weight= 5, uniform= 'a')

input.grid(row= 0, columnspan= 2, sticky= 'nsew')

root.mainloop()
        


