import requests
from django.conf import settings
from django.shortcuts import render

def weather_view(request):
    weather_data = None
    error = None

    if request.method == 'POST':
        city = request.POST.get('city')
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={settings.KEY}&units=metric"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            rain = data.get('rain', {}).get('1h', 0)
            snow = data.get('snow', {}).get('1h', 0)

            from datetime import datetime
            sunrise = datetime.utcfromtimestamp(data['sys']['sunrise'] + data['timezone']).strftime('%H:%M')
            sunset = datetime.utcfromtimestamp(data['sys']['sunset'] + data['timezone']).strftime('%H:%M')

            weather_data = {
                'city': city.title(),
                'temperature': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'description': data['weather'][0]['description'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'wind_speed': data['wind']['speed'],
                'icon': data['weather'][0]['icon'],
                'clouds': data['clouds']['all'],
                'rain': rain,
                'snow': snow,
                'sunrise': sunrise,
                'sunset': sunset,
            }
        else:
            error = "City not found"

    return render(request, 'weather.html', {
        'weather_data': weather_data,
        'error': error
    })
