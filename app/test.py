import requests
import pprint

KEY = 'af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir'


region = 'Москва'
query = 'Укулеле'


# getting location id
resp = requests.get(
        "https://m.avito.ru/api/1/slocations",
        params={
            "key": KEY,
            "q": region
        }
    )
counties_list = resp.json()["result"]["locations"]
for item in counties_list:
    if item["names"]["1"] == region:
        location_id = item["id"]
        break
#print(location_id)

# getting number of
resp = requests.get(
        "https://m.avito.ru/api/9/items",
        params={
            "key": KEY,
            "query": query,
            "locationId": location_id
        }
    )

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(resp.json())
json_response = resp.json()
top_ad_titile = json_response['result']['items'][0]['value']['title']
top_ad = json_response['result']['items'][0]['value']['uri_mweb']
result = resp.json()['result']['mainCount']

print("https://m.avito.ru/"+top_ad, top_ad_titile)
#print(result)

#location_id = resp_json["result"]["locations"]["id"]

#print(location_id)

d = {"2020-12-13T14:14:56.073875":{"ad count":47350,"top ads":[{"ad_title":"Велосипед на литых","ad_uri":"https://www.avito.ru//moskva/velosipedy/velosiped_na_lityh_2056541403"},{"ad_title":"Велосипед скоростной новый","ad_uri":"https://www.avito.ru//moskva/velosipedy/velosiped_skorostnoy_novyy_2024291977"},{"ad_title":"Красивый Велосипед Dinos 29'' Колеса 29\"","ad_uri":"https://www.avito.ru//moskva/velosipedy/krasivyy_velosiped_dinos_29_kolesa_29_2039901190"},{"ad_title":"Enduro/Trail Yeti sb130 turq x01","ad_uri":"https://www.avito.ru//moskva/velosipedy/endurotrail_yeti_sb130_turq_x01_2003928130"}]},"2020-12-13T14:15:57.104270":{"ad count":47350,"top ads":[{"ad_title":"Велосипед скоростной новый","ad_uri":"https://www.avito.ru//moskva/velosipedy/velosiped_skorostnoy_novyy_2024291977"},{"ad_title":"Велосипед","ad_uri":"https://www.avito.ru//moskva/velosipedy/velosiped_2021654523"},{"ad_title":"Велосипед на литых","ad_uri":"https://www.avito.ru//moskva/velosipedy/velosiped_na_lityh_2056541403"},{"ad_title":"Велосипед Trek Y26","ad_uri":"https://www.avito.ru//moskva/velosipedy/velosiped_trek_y26_2063468189"}]}}

pp.pprint(d)
