import requests
import re
import os
import csv
import sys
import json

#SOURCE: I DO NOT CLAIM THE RIGHTS TO THE DATA PROVIDED: IT IS ENTIRELY IN THE POSSESSION
#OF A WEBSITE, CALLED TIMEANDDATE.COM. LINK: https://www.timeanddate.com

weather_frontpage_url = "https://www.timeanddate.com/weather/?low=c"
weather_directory = os.path.join(sys.path[0], 'Weather_save')
frontpage_filename = "weather_fp.html"



re_pick_links_block = re.compile(
    r'<table class="zebra fw tb-wt va-m"><thead><tr>(.*)</span></p></div></div>', flags=re.DOTALL
    )

re_pick_links = re.compile(
    r'\<a\shref\="/weather(.*?)">', flags=re.DOTALL
    )

re_names_from_links = re.compile(
    r'/(?P<country>.*?)/(?P<city>.*)', flags=re.DOTALL
    )

re_info = re.compile(
    # COUNTRY AND CITY
    r'Weather<\/a> &nbsp; <a target=_top href="\/weather\/(?P<country>.*?)'
    r'\/(?P<city>.*?)"'
    r'.*?'
    # CURRENT TEMPERATURE
    r'class=h2>(?P<temp>.+?)<\/div>'
    r'.*?'
    # CURRENT WEATHER
    r'<p>(?P<weather>.+?)<'
    r'.*?'
    # WIND
    r'Wind:\s(?P<wind>.+?)<\/p>'
    r'.*?'
    # VISIBILITY
    r'class=four>Visibility:\s<\/span>\s(?P<visibility>.+?)<\/p><p>'
    r'.*?'
    # PRESSURE
    r'Pressure:\s<\/span>\s(?P<pressure>.+?)<\/p>'
    r'.*?'
    # HUMIDITY
    r'Humidity:\s<\/span>\s(?P<humidity>.+?)<'
    r'.*?'
    # DEW POINT
    r'Dew Point:\s<\/span>\s(?P<dewpoint>.+?)<\/p>'
    r'.*?'
    # AFTER A DAY
    # -----------
    # TEMPERATURE
    r'<div class="row pdflexi">.*?</td><td class="sep" >(?P<ntemp>.+?)<'
    r'.*?'
    # WIND
    r'<td>(?P<nwind>.+?)<\/td>'
    r'.*?'
    # HUMIDITY
    r'</td><td>(?P<nhumidity>.+?)<\/td>'
    , flags=re.DOTALL)
    


def download_url_to_string(url):
    try:
        r = requests.get(url)
        text = r.text
    except requests.exceptions.RequestException as error:
        print(error)
        text = None
    return text

def save_string_to_file(text, directory, filename):
    os.makedirs(directory, exist_ok=True)
    path_fp = os.path.join(directory, filename)
    with open(path_fp, 'w', encoding='utf-8') as file_out:
        file_out.write(text)
    return None

def save_frontpage():
    string = download_url_to_string(weather_frontpage_url)
    save_string_to_file(string, weather_directory, frontpage_filename)
    return None

def save_pages_to_file():
    with open(os.path.join(weather_directory, frontpage_filename), 'r', encoding='utf-8') as fp:
        text = fp.read()
    block = re_pick_links_block.findall(text)[0]
    links = re_pick_links.findall(block)
    print(links)
    for link in links:
        page = requests.get('https://www.timeanddate.com/weather' + link + "/ext")
        names_dict = re_names_from_links.search(link)
        print(names_dict)
        filename = '{}_{}.html'.format(names_dict['country'], names_dict['city'])
        full_filepath = os.path.join(weather_directory, filename)
        with open(full_filepath, 'w', encoding='utf-8') as save:
            save.write(page.text)
    return None

def read_inf():
    inf = []
    for filename in os.listdir(weather_directory):
        if filename != 'weather_fp.html':
            full_path = os.path.join(weather_directory, filename)
            with open(full_path, encoding='utf-8') as file:
                content = file.read()
                inf.append(get_inf(content))
        else:
            continue
    return inf
    
    
def uppercase_every_first_letter(string):
    new_string=''
    splitted_words = string.split(' ')
    for word in splitted_words:
        i = 0
        for letter in list(word):
            if word == 'and' or word == 'of':
                new_string += letter
            elif i == 0:
                new_string += letter.upper()
                i +=1
            else:
                new_string += letter
        new_string += ' '
    return new_string[:-1]
                
                



def get_inf(text):
    matching = re_info.search(text)
    if matching:
        inf = matching.groupdict()
        if inf['temp'] != 'N/A':
            if inf['temp'][0] == '-':
                inf['temp'] = '-' + re.search(r'\d+', inf['temp']).group()
            else:
                inf['temp'] = int(re.search(r'\d+', inf['temp']).group())
        else:
            inf['temp'] = None
        if inf['wind'] != 'N/A':
            if inf['wind'] != 'No wind':
                inf['wind'] = re.search(r'\d+', inf['wind']).group()
        else:
            inf['wind'] = None
        if inf['visibility'] != 'N/A':
            inf['visibility'] = re.search(r'\d+', inf['visibility']).group()
        else:
            inf['visibility'] = None
        if inf['pressure'] != 'N/A':
            inf['pressure'] = re.search(r'\d+', inf['pressure']).group()
        else:
            inf['pressure'] = None
        if inf['humidity'] != 'N/A':
            inf['humidity'] = re.search(r'\d+', inf['humidity']).group()
        else:
            inf['humidity'] = None
        if inf['dewpoint'] != 'N/A':
            if inf['dewpoint'][0] == '-':
                inf['dewpoint'] = '-' + re.search(r'\d+', inf['dewpoint']).group()
            else:
                inf['dewpoint'] = int(re.search(r'\d+', inf['dewpoint']).group())
        else:
            inf['dewpoint'] = None
        cities = inf['city'].split("-")
        inf['city'] = " ".join(cities)
        countries = inf['country'].split("-")
        inf['country'] = " ".join(countries)               
        inf['city'] = uppercase_every_first_letter(inf['city'])
        inf['country'] = uppercase_every_first_letter(inf['country'])
        if inf['nwind'] != 'N/A':
            if inf['nwind'] != 'No wind':
                inf['nwind'] = re.search(r'\d+', inf['nwind']).group()
        else:
            inf['nwind'] = None
        if inf['ntemp'] != 'N/A':
            if inf['ntemp'][0] == '-':
                inf['ntemp'] = '-' + re.search(r'\d+', inf['ntemp']).group()
            else:
                inf['ntemp'] = int(re.search(r'\d+', inf['ntemp']).group())
        else:
            inf['ntemp'] = None
        if inf['nhumidity'] != 'N/A':
            inf['nhumidity'] = re.search(r'\d+', inf['nhumidity']).group()
        else:
            inf['nhumidity'] = None
        return inf
    
    
    else:
        print("CAN'T READ")
        print(text)
        exit()

data = read_inf()

from pprint import pprint

with open('information.csv', 'w') as file:
    writer = csv.DictWriter(file, ['country', 'city', 'temp', 'weather',
                                   'wind', 'visibility', 'pressure',
                                   'humidity', 'dewpoint', 'ntemp', 'nwind', 'nhumidity'])
    writer.writeheader()
    for inf in data:
        writer.writerow(inf)

    
                    
