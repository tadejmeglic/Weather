import requests
import re
import os
import csv

weather_frontpage_url = "https://www.timeanddate.com/weather/?low=c"
weather_directory = "C:/Users/tadej/Documents/GitHub/Weather/Weather_save"
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
        page = requests.get('https://www.timeanddate.com/weather' + link)
        names_dict = re_names_from_links.search(link)
        print(names_dict)
        filename = '{}_{}.html'.format(names_dict['country'], names_dict['city'])
        full_filepath = os.path.join(weather_directory, filename)
        with open(full_filepath, 'w', encoding='utf-8') as save:
            save.write(page.text)
    return None
        

                    