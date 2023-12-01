import requests
from django.shortcuts import render
from datetime import datetime

def index(request):
    try:
        if request.method == 'POST':
            API_KEY = '3ac8030d435340805fb457e2b81d7467'
            city_name = request.POST.get('city')
            
            # Get current weather data
            current_url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric'
            current_response = requests.get(current_url)
            current_data = current_response.json()

            # Check if the API call was successful
            if current_response.status_code == 200:
                # Get 5-day forecast data
                forecast_url = f'https://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={API_KEY}&units=metric'
                forecast_response = requests.get(forecast_url)
                forecast_data = forecast_response.json()

                # Check if the forecast API call was successful
                if forecast_response.status_code == 200:
                    # get relevant information from the API responses
                    current_temperature = round(current_data['main']['temp'])
                    current_description = current_data['weather'][0]['description'].capitalize()
                    current_icon = current_data['weather'][0]['icon']
                    current_time = datetime.now().strftime("%A, %B %d %Y, %I:%M %p")

                    # get forecast information for the 5 days forecast
                    days_forecast = []
                    today = datetime.now()
                    for entry in forecast_data['list']:
                        date = datetime.fromtimestamp(entry['dt'])
                        # Check if the entry is within the next 5 days
                        if date > today and (date - today).days < 5:
                            temperature = round(entry['main']['temp'])
                            description = entry['weather'][0]['description'].capitalize()
                            icon = entry['weather'][0]['icon']

                            entry_weekday = date.strftime("%A, %I:%M %p")

                            days_forecast.append({
                                'weekdays': entry_weekday, 
                                'temperature': f'{temperature}°C', 
                                'description': description, 
                                'icon': icon
                                })

                    city_weather_update = {
                        'city': city_name,
                        'description': current_description,
                        'icon': current_icon,
                        'temperature': f'{current_temperature}°C',
                        'country_code': current_data['sys']['country'],
                        'wind': str(current_data['wind']['speed']) + ' km/h',
                        'humidity': str(current_data['main']['humidity']) + '%',
                        'time': current_time
                    }

                    context = {'city_weather_update': city_weather_update, 'forecast_data': days_forecast, 'error_message': None}
                    return render(request, 'index.html', context)
                else:
                    # Print error details for forecast API
                    print(f"Forecast API Error: {forecast_response.status_code} - {forecast_response.text}")
            else:
                # Print error details for current weather API
                print(f"Current Weather API Error: {current_response.status_code} - {current_response.text}")
                
        else:
            # Handle the case where the request is not a POST
            city_weather_update = {}
            days_forecast = []

        context = {'city_weather_update': city_weather_update, 'forecast_data': days_forecast, 'error_message': None}
        return render(request, 'index.html', context)

    except Exception as e:
        # Handle generic exception
        error_message = f"The City you've entered is not found."
        context = {'error_message': error_message}
        return render(request, 'index.html', context)
