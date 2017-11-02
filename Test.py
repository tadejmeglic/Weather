import requests
import re
import os
import csv


text = '''<tbody><tr><td><a
href="https://www.timeanddate.com/weather/united-arab-emirates/abu-dhabi">Abu
Dhabi</a><span id="p0s" class="wds"></span></td><td id="p0"
class="r">Thu 17:59</td><td class="r"><img src="./Temperatures and
Weather in Capitals Worldwide_files/wt-1.png" alt="Sunny. Hot."
title="Sunny. Hot." width="40" height="40"></td><td
class="rbi">32&nbsp;°C</td><td><a
href="https://www.timeanddate.com/weather/nicaragua/managua">Managua</a><span
id="p97s" class="wds"></span></td><td id="p97" class="r">Thu
07:59</td><td class="r"><img src="./Temperatures and Weather in Capitals
Worldwide_files/wt-2.png" alt="Scattered clouds. Warm." title="Scattered
clouds. Warm." width="40" height="40"></td><td
class="rbi">26&nbsp;°C</td></tr><tr><td><a
href="https://www.timeanddate.com/weather/ghana/accra">Accra</a><span
id="p1s" class="wds"></span><, flags=re.DOTALL)'''

message = re.search(r'<a href=(.*?)class', text, flags=re.DOTALL)
