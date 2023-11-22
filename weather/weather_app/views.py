import requests
from django.shortcuts import render
#from datetime import datetime

# Create your views here.

def get_weather(api_key, city, country):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={api_key}'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        # Handle the case where the API request was not successful
        return None
    
def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

def index(request):
    api_key = '3ac8030d435340805fb457e2b81d7467'
    city = request.GET.get('city', 'Butuan City')  
    country = request.GET.get('country', 'Philippines') 
    weather_data = get_weather(api_key, city, country)
    
    if weather_data:
        # Check if the response includes temperature data
        if 'main' in weather_data and 'temp' in weather_data['main']:
            temperature_kelvin = weather_data['main']['temp']
            temperature_celsius = round(kelvin_to_celsius(temperature_kelvin))
        else:
            temperature_celsius = 'N/A'

        humidity = weather_data.get('main', {}).get('humidity', 'N/A')
        wind_speed_meters_per_second = weather_data.get('wind', {}).get('speed', 'N/A')

        # Convert wind speed from m/s to km/h
        wind_speed_kilometers_per_hour = round(wind_speed_meters_per_second * 3.6)

        description = weather_data.get('weather', [{}])[0].get('description', 'N/A')
    else:
        # Handle the case where weather data is not available
        temperature_celsius = 'N/A'
        humidity = 'N/A'
        wind_speed_kilometers_per_hour = 'N/A'
        description = 'N/A'

    context = {
        'city': city,
        'country': country,
        'temperature': temperature_celsius,
        'humidity': humidity,
        'wind_speed': wind_speed_kilometers_per_hour,  # Display wind speed in km/h
        'description': description,
    }
    return render(request, 'index.html', context)