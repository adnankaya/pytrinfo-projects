from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"weather-websocket-data/$", consumers.WeatherConsumer.as_asgi()),
]