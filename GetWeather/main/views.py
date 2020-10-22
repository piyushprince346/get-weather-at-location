from django.shortcuts import render
from django.http import HttpResponse

import requests


def get_html_content(city):
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    city = city.replace(' ','+')
    content = session.get(f'https://www.google.com/search?q=weather+in+{city}').text
    return content

# Create your views here.
def home(request):
    weather = {}
    a = 1
    if 'city' in request.GET:
        # fetching the weather data from google weather
        city_name = request.GET['city']
        content = get_html_content(city_name)

        # using beautiful soup 
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(content, 'html.parser')
        try:
            weather['location'] = soup.find('div', attrs={'id': 'wob_loc'}).text
            weather['time'] = soup.find('div', attrs={'id': 'wob_dts'}).text
            weather['weather_condition'] = soup.find('span', attrs={'id': 'wob_dc'}).text
            weather['temperature'] = soup.find('span', attrs={'id': 'wob_tm'}).text
            weather['precipitation'] = soup.find('span', attrs={'id': 'wob_pp'}).text
            weather['humidity'] = soup.find('span', attrs={'id': 'wob_hm'}).text
            weather['wind'] = soup.find('span', attrs={'id': 'wob_ws'}).text
        except:
            a = 0
        
    return render(request,'index.html',{'weather' : weather,'a' : a})
