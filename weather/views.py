import requests
from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm
import json

url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=664c2edc953073e814baa70200e58200'
forecast_url = 'http://api.openweathermap.org/data/2.5/forecast?q={}&units=imperial&appid=664c2edc953073e814baa70200e58200'

def getWeatherInfo(city):
    r = requests.get(url.format(city)).json()

    city_weather = {
        'city' : city,
        'temperature' : r['main']['temp'],
        'description' : r['weather'][0]['description'],
        'icon' : r['weather'][0]['icon'],
    }

    return (city_weather)

def getWeatherInfoByLatLon(lat,lon):
    url_lat = 'http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&units=imperial&appid=664c2edc953073e814baa70200e58200'
    r = requests.get(url_lat.format(lat,lon)).json()

    city_weather = {
        'city' : r['name'],
        'temperature' : r['main']['temp'],
        'description' : r['weather'][0]['description'],
        'icon' : r['weather'][0]['icon'],
    }

    return (city_weather)


def index(request):

    weather_data = []
    current_weather_data = []

    #we can use below method if application is hosted in server. this is correct procedure
    # x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    # if x_forwarded_for:
    #     ip = x_forwarded_for.split(',')[0]
    # else:
    #     ip = request.META.get('REMOTE_ADDR')

    #currently i am using localhost for testing so i am getting my public ip using below URL. 
    #if we hosted in server below api always takes server ip. this will not suit for prod deployment
    client_ip = requests.get("https://api.ipify.org?format=json").json()['ip']

    geoLocation = requests.get("http://ip-api.com/json/{}".format(client_ip)).json()

    response_geolocation = getWeatherInfoByLatLon(geoLocation['lat'],geoLocation['lon'])

    forecast_response = requests.get(forecast_url.format(geoLocation['city'])).json()

    count = 1
    for inc in forecast_response['list']:
        if "00:00:00" in inc['dt_txt']:
            response_geolocation['day'+str(count)] = [inc['dt_txt'].split()[0],inc['main']['temp']]
            count = count + 1

    current_weather_data.append(response_geolocation)

    if request.method == 'POST':
        city = request.POST['city']

        city_weather = getWeatherInfo(city)

        forecast_response = requests.get(forecast_url.format(city)).json()

        count = 1
        for inc in forecast_response['list']:
            if "00:00:00" in inc['dt_txt']:
                city_weather['day'+str(count)] = [inc['dt_txt'].split()[0],inc['main']['temp']]
                count = count + 1

        weather_data.append(city_weather)

    context = {
        'weather_data' : weather_data, 
        'current_weather_data' : current_weather_data
    }

    return render(request, "weather/index.html", context)

def add(request):
    
    err_msg = ''
    message = ''
    message_class = ''

    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()
            
            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()

                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'City does not exist in the world!'
            else:
                err_msg = 'City already exists in the database!'

        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = 'City added successfully!'
            message_class = 'is-success'

    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:

        r = requests.get(url.format(city)).json()

        city_weather = {
            'city' : city.name,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }

        forecast_response = requests.get(forecast_url.format(city)).json()

        count = 1
        for inc in forecast_response['list']:
            if "00:00:00" in inc['dt_txt']:
                city_weather['day'+str(count)] = [inc['dt_txt'].split()[0],inc['main']['temp']]
                count = count + 1

        weather_data.append(city_weather)

    context = {
        'weather_data' : weather_data, 
        'form' : form,
        'message' : message,
        'message_class' : message_class
    }

    return render(request, 'weather/weather.html', context)

def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    
    return redirect('add')