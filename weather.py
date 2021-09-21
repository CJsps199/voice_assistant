import requests
from pprint import pprint

url = 'http://api.openweathermap.org/data/2.5/forecast?id=938694&appid=7a4e25d9875abca76452bd084f8c1ce7&units=metric'

res = requests.get(url)

data = res.json()
pprint(data)
# temp = data['main']['temp']
# humidity = data['main']['humidity']
# weather = data['weather'][0]['description']
# clouds = data['clouds']['all']
# pprint(temp)
# pprint(humidity)
# pprint(weather)
# pprint(clouds)