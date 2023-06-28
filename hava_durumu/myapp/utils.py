import requests
from django.conf import settings


def request_to_weatherapi(city: str) -> dict:
    URL = f"http://api.weatherapi.com/v1/current.json?key={settings.WA_APIKEY}&q={city}"
    res = requests.get(URL)
    res.raise_for_status()  # Raise an exception for non-200 status codes
    res_json = res.json()
    return {
        "city": res_json["location"]["name"],
        "description": res_json["current"]["condition"]["text"],
        "icon": f'http:{res_json["current"]["condition"]["icon"]}',
        "temperature": res_json["current"]["temp_c"],
        "updated_date": res_json["current"]["last_updated"],
        "api_response": res.text
    }
