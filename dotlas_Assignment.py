import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

restaurant_name = []
restaurant_logo = []
latitude = []
longitude = []
cuisine_tags = []
menu_items = []

# List of links of 10 restaurants
links = ['https://www.talabat.com/uae/restaurant/621133/ginos-deli-jlt?aid=1308',
         'https://www.talabat.com/uae/restaurant/645430/pasta-della-nona-jlt-jumeirah-lakes-towers?aid=1308',
         'https://www.talabat.com/uae/restaurant/50445/pizzaro-marina-3?aid=1308',
         'https://www.talabat.com/uae/restaurant/605052/the-pasta-guyz-dubai-marina?aid=1308',
         'https://www.talabat.com/uae/restaurant/621796/pizza-di-rocco-jumeirah-lakes-towers--jlt?aid=1308',
         'https://www.talabat.com/uae/restaurant/665714/affordabowls-khalifa-city?aid=1483',
         'https://www.talabat.com/uae/restaurant/47249/kabab-grill-madinat-khalifa-a?aid=1483',
         'https://www.talabat.com/uae/restaurant/665630/starbucks-masdar-city?aid=1483',
         'https://www.talabat.com/uae/restaurant/663723/sushi-house-masdar-city?aid=1483',
         'https://www.talabat.com/uae/restaurant/47216/the-cheesecake-factory-yas-island?aid=1483'
        ]

for i in range(0, len(links)):  
    r = requests.get(links[i])
    soup = BeautifulSoup(r.content,'html.parser')
    scripts = soup.find('script', type='application/ld+json')
    data = json.loads(scripts.text)

    if (data['@type'] != 'Restaurant'):
        continue
  
    restaurant_name.append( data['name'] )
    restaurant_logo.append( data['image'] )
    latitude.append( data['geo']['latitude'] )
    longitude.append( data['geo']['longitude'] )
    cuisine_tags.append( data['servesCuisine'] )

    menu = soup.find('script', type = 'application/json')
    menu = json.loads(menu.text)
    menu_data= menu['props']['pageProps']['initialMenuState']['menuData']['items']
    temp = []
    for j in range(0, len(menu_data)):
        temp.append(
            [menu_data[j]['name'], menu_data[j]['description'],menu_data[j]['price'], menu_data[j]['image']]
        )
    menu_items.append(temp)
    
table = {
  "restaurant_name": restaurant_name,
  "restaurant_logo": restaurant_logo,
  "latitude": latitude,
  "longitude": longitude,
  "cuisine_tags": cuisine_tags,
  "menu_items": menu_items
}

df = pd.DataFrame(table) 

df.to_csv('10_restaurants.csv')
print(df)
