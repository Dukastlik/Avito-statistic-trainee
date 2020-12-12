import requests


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
print(location_id)

# getting number of
resp = requests.get(
        "https://m.avito.ru/api/9/items",
        params={
            "key": KEY,
            "query": query,
            "locationId": location_id
        }
    )

result = resp.json()['result']['mainCount']
print(result)

#location_id = resp_json["result"]["locations"]["id"]

#print(location_id)