import requests
import re
import os
import csv

weather_frontpage_url = "https://www.timeanddate.com/"
weather_directory = "U:\Programiranje 1\Projektna\Weather\Weather_save"
frontpage_filename = "weather_fp.html"

def download_url_to_string(url):
    try:
        r = requests.get(url)
        text = r.text
    except requests.exceptions.RequestException as error:
        print(error)
        text = None
    return text

def save_string_to_file(text, directory, filename):
    os.makedirs(directory, exists_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w') as file_out:
        file_out.write(text)
    return None

def save_frontpage():
    string = download_url_to_string(weather_frontpage_url)
    save_string_to_file(string, weather_directory, frontpage_filename)
    return None

def save_page(country, city):
    string = download_url_to_string("https://www.timeanddate.com/weather/" + str(country) + "/" + str(city) + "/hourly")
    save_string_to_file(string, weather_directory, "Weather_"+country+"_"+city)
    return None
        

                    
