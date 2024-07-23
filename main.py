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
placeHolderText = "Search for new Cities"
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
description = None
windSpeed = None
clouds = 0
only_currentTime = None
sunsetTime = None
sunriseTime = None

def kelvinToCelciusAndFahrenheit(kelvin) :
    celsius = kelvin -273.15
    fahrenheit = (celsius * (9/5)) + 32
    return celsius, fahrenheit

def setData(city): 
    global tempFahrenheit, tempCelsius, feelsLikeTempFahrenheit, feelsLikeTempCelsius, tempMinCelsius, tempMinFahrenheit, tempMaxCelsius, tempMaxFahrenheit
    global pressure, humidity, seaLevel, description, windSpeed, clouds
    global sunriseTime, sunsetTime, only_currentTime

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

#create separate function for data req for background if needed
def set_background() :
    global background_image, label1
    image_path = ""

    # Get the directory of the current script
    script_dir = os.path.dirname(__file__)

    if clouds > 50 :
        image_path = os.path.join(script_dir, "backgrounds", "rainybackground.jpg")
    elif (only_currentTime > sunsetTime) or (only_currentTime < sunriseTime):
        image_path = os.path.join(script_dir, "backgrounds", "Nightbackground.jpeg")
    else :     
        image_path = os.path.join(script_dir, "backgrounds", "Sunnybackground.jpg")

    if not os.path.exists(image_path):
        print(f"Error: The file '{image_path}' does not exist.")
    else:
        image = Image.open(image_path)
        resized_image = image.resize((525,775))
        background_image = ImageTk.PhotoImage(resized_image)
        canvas = tk.Canvas(root, width=resized_image.width, height=resized_image.height)
        canvas.grid(row=0, column=0, columnspan=2, rowspan=7, sticky="nsew")
        canvas.create_image(0, 0, anchor="nw", image=background_image)
        canvas.lower("all")
    
def search(event=None):
    global CITY
    CITY = input.get()
    setData(CITY)
    set_background()

    url = BASE_URL + "appid=" + API_KEY + "&q=" + CITY
    response = requests.get(url).json()

    #labels
    cityLabel = tk.Label(root, text= f"{CITY}", background= 'pink', font= ('Roman',25))
    temp = tk.Label(root, text= f"{tempFahrenheit:.2f}°F", background= 'pink', font= ('Roman',70))
    feelsTemp = tk.Label(root, text= f"Feels Like Temperature: {feelsLikeTempFahrenheit:.2f}°F", background= 'pink', font= ('Roman',25))
    pressureLabel = tk.Label(root, text= f"Pressure: {pressure}", background= 'pink', font= ('Roman',25))
    humidityLabel = tk.Label(root, text= f"Humidity: {humidity}", background= 'pink', font= ('Roman',25))
    seaLevelLabel = tk.Label(root, text= f"Sea Level: {seaLevel}", background= 'pink', font= ('Roman',25))
    descriptionLabel = tk.Label(root, text= f"{description}", background= 'pink', font= ('Roman',25))
    windSpeedLabel = tk.Label(root, text= f"WindSpeed: {windSpeed}", background= 'pink', font= ('Roman',25))
    lowTempLabel = tk.Label(root, text= f"L: {tempMinFahrenheit:.2f}°F", background= 'pink', font= ('Roman',25))
    highTempLabel = tk.Label(root, text= f"H: {tempMaxFahrenheit:.2f}°F", background= 'pink', font= ('Roman',25))

    #grid
    cityLabel.grid(row=1, columnspan= 2, sticky= 'sew', padx= 0, pady= 0)
    temp.grid(row= 2, columnspan= 2, sticky= 'new', padx= 0, pady= 0)
    feelsTemp.grid(row= 3, columnspan= 2, sticky= 'nsew')
    lowTempLabel.grid(row= 4, column= 0, sticky= 'nse')
    highTempLabel.grid(row= 4, column= 1, sticky= 'nsw')   
    descriptionLabel.grid(row= 5, columnspan= 2, sticky= 'new')

    pressureLabel.grid(row= 6, column= 0, sticky= 'nsew')
    humidityLabel.grid(row= 6, column= 1, sticky= 'nsew')
    seaLevelLabel.grid(row= 7, column= 0, sticky= 'nsew')
    windSpeedLabel.grid(row= 7, column= 1, sticky= 'nsew')

    print(response)

def on_focus_in(event):
    if input.get() == placeHolderText:
        input.delete(0, tk.END)
        input.config(fg='black')

def on_focus_out(event):
    if input.get() == '':
        input.insert(0, placeHolderText)
        input.config(fg='gray')

def search_on_enter(event):
    search()
    input.delete(0, tk.END)

def on_click_outside(event):
    #Check if the click is outside the input widget
    if not input.winfo_containing(event.x_root, event.y_root) == input:
        root.focus_set()

#Window 
root = tk.Tk()
root.title('Weather App')
root.geometry('500x750')

#input

input = tk.Entry(root, font = ('Arial', 15), fg= 'gray')
input.insert(0, placeHolderText)
input.bind('<FocusIn>', on_focus_in)
input.bind('<FocusOut>', on_focus_out)
input.bind('<Return>', search_on_enter)

#Bind mouse click outside the input widget to root window
root.bind('<Button-1>', on_click_outside)
        
#grid

root.columnconfigure(0, weight= 1, uniform= 'a')
root.columnconfigure(1, weight= 1, uniform= 'a')

root.rowconfigure(0, weight= 1, uniform= 'a')
root.rowconfigure(1, weight= 0, uniform= 'a')
root.rowconfigure((2), weight= 6, uniform= 'a')
root.rowconfigure((3,4,5), weight= 2, uniform= 'a')
root.rowconfigure((6,7), weight= 5, uniform= 'a')

input.grid(row= 0, columnspan= 2, sticky= 'nsew')

root.mainloop()
