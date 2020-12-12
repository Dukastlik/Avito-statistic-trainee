import requests



KEY = 'af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir'

query = "лопата"
locationId = "637640"


def get_sugested_uri(query, locationId):

    resp = requests.post(
            "https://m.avito.ru/api/3/suggests",
            params={"key": KEY},
            data={
                "key": KEY,
                "locationId": locationId,
                "query": query,
            }
        )
    print(resp.json())
    uri = resp.json()['result'][0]['uri']
    uri = uri.split('/')
    print(uri[-1][7:])

    resp = requests.get(
        "https://m.avito.ru/api/9/items?"+"key="+KEY+"&"+uri[-1][7:]
    )
    print(resp)
    ad_count = resp.json()['result']['mainCount']
    print(ad_count)

get_sugested_uri(query, locationId)