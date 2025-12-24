import requests
import os


#weather api
def get_weather(getCity):
    city = getCity
    weather_key = os.environ.get('WEATHER_API')
    url = f"http://api.weatherapi.com/v1/current.json?key={weather_key}&q={city}"
    res = requests.get(url)
    
    if res.status_code == 200 :
        wdict = res.json()
        
        loc = wdict["location"]
        cur  = wdict["current"]
        return loc , cur
    else : 
        return "City not found"