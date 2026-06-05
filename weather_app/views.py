from django.shortcuts import render
from django.conf import settings
import requests

# Create your views here.
def home(request):
    weather_data = None
    error = None
    forecast_data = []

    if request.method == 'POST':
        city = request.POST.get('city')
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={settings.WEATHER_API_KEY}&units=metric"
        
        response = requests.get(url).json()
        if response['cod'] == 200:
            weather_data = {
            'city': response['name'],
            'country': response['sys']['country'],
            'temperature': round(response['main']['temp']),
            'feels_like': round(response['main']['feels_like']),
            'humidity': response['main']['humidity'],
            'pressure': response['main']['pressure'],
            'wind_speed': response['wind']['speed'],
            'description': response['weather'][0]['description'].title(),
            'icon': response['weather'][0]['icon'],
            'visibility': response.get('visibility', 0),
            'clouds': response['clouds']['all'],
            }

        forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={settings.WEATHER_API_KEY}&units=metric"
        forecast_response = requests.get(forecast_url).json()
        
        seen_dates = []
        for item in forecast_response['list']:
                date = item['dt_txt'].split(' ')[0]
                if date not in seen_dates:
                    seen_dates.append(date)
                    forecast_data.append({
                        'date': date,
                        'temp_max': round(item['main']['temp_max']),
                        'temp_min': round(item['main']['temp_min']),
                        'description': item['weather'][0]['description'].title(),
                        'icon': item['weather'][0]['icon'],
                        'humidity': item['main']['humidity'],
                    })

        # Only keep 5 days
        forecast_data = forecast_data[:5]

    else:
        error = "City no found. Please try again."
        
    return render(request, 'index.html', {
        'weather': weather_data,
        'forecast': forecast_data,
        'error': error,
    })