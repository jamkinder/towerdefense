import requests
response = requests.get("http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode=Государственный исторический музей &format=json")
somelist = (response.json()['response']['GeoObjectCollection']['featureMember'])
somelist2 = somelist[0]
print(somelist2['GeoObject']['metaDataProperty']['GeocoderMetaData']['Address'])
print(somelist2['GeoObject']['boundedBy'])
print(somelist2['GeoObject']['Point'])