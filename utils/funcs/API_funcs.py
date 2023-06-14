import requests
from config_data.config import RAPID_API_KEY


def get_request(method_endswith, params):
    url = f"https://hotels4.p.rapidapi.com/{method_endswith}"
    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"}

    response = requests.get(
        url,
        params=params,
        timeout=15,
        headers=headers
    )
    if response.status_code == requests.codes.ok:
        return response.json()


def post_request(method_endswith, params):
    url = f"https://hotels4.p.rapidapi.com/{method_endswith}"
    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
        "content-type": "application/json"
    }

    response = requests.post(
        url,
        json=params,
        timeout=15,
        headers=headers
    )

    if response.status_code == requests.codes.ok:
        return response.json()


def get_location_id(q):
    params = {'q': q, 'locale': 'ru_RU'}
    data = get_request('locations/v3/search', params)

    try:
        sr = data['sr']
        for item in sr:
            if item['type'] == 'CITY':
                return item['gaiaId']
    except:
        pass


def get_hotels_ids(location_id, count=3, sort='PRICE_LOW_TO_HIGH'):
    params = {'currency': 'RUB',
              'eapid': 1,
              'locale': 'ru_RU',
              'siteId': 300000001,
              'destination': {
                  'regionId': location_id
              },
              'checkInDate': {'day': 7, 'month': 7, 'year': 2023},
              'checkOutDate': {'day': 9, 'month': 7, 'year': 2023},
              'rooms': [{'adults': 1}],
              'resultsStartingIndex': 0,
              'resultsSize': count,
              'sort': sort,
              'filters': {'availableFilter': 'SHOW_AVAILABLE_ONLY'}
              }
    try:
        data = post_request('properties/v2/list', params)
        return [h['id'] for h in data['data']['propertySearch']['properties']]
    except:
        pass


def get_hotel_detail(hotel_id):
    params = {'currency': 'RUB',
              'eapid': 1,
              'locale': 'ru_RU',
              'siteId': 300000001,
              'propertyId': hotel_id
              }
    try:
        data = post_request('properties/v2/detail', params)
        res = dict()
        res['name'] = data['data']['propertyInfo']['summary']['name']
        res['tagline'] = data['data']['propertyInfo']['summary']['tagline']
        res['address'] = data['data']['propertyInfo']['summary']['location']['address']['firstAddressLine']
        res['image_url'] = data['data']['propertyInfo']['propertyGallery']['images'][0]['image']['url']
        res['image_description'] = data['data']['propertyInfo']['propertyGallery']['images'][0]['image']['description']
        return res
    except:
        pass
