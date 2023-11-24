import requests
from django.shortcuts import render
from datetime import datetime

# Create your views here.
def index(request):
    # if there are no errors the code inside try will execute
    try:
    # checking if the method is POST
        if request.method == 'POST':
            API_KEY = '3ac8030d435340805fb457e2b81d7467'
            # getting the city name from the form input   
            city_name = request.POST.get('city')
            # the url for current weather, takes city_name and API_KEY   
            url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric'
            # converting the request response to json   
            response = requests.get(url).json()
            # getting the current time
            current_time = datetime.now()
            # formatting the time using directives, it will take this format Day, Month Date Year, Current Time 
            formatted_time = current_time.strftime("%A, %B %d %Y, %H:%M:%S %p")
            # bundling the weather information in one dictionary
            city_weather_update = {
                'city': city_name,
                'description': response['weather'][0]['description'],
                'icon': response['weather'][0]['icon'],
                'temperature':str(response['main']['temp']) + ' °C',
                'country_code': response['sys']['country'],
                'wind': (response['wind']['speed']),
                'humidity':str(response['main']['humidity']),
                'time': formatted_time
            }
        # if the request method is GET empty the dictionary
        else:
            city_weather_update = {}
        
        context = {'city_weather_update': city_weather_update, 'error_message': None}
        return render(request, 'index.html', context)
    except Exception as e:
        # Handle generic exception
        error_message = f"The city you've enter is not found!"
        context = { 'error_message': error_message}
        return render(request, 'index.html', context)

