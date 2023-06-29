import json
# comes from django channels
from channels.generic.websocket import WebsocketConsumer

active_consumers = []

class WeatherConsumer(WebsocketConsumer):
    def connect(self):
        active_consumers.append(self)
        self.accept()

    def disconnect(self, close_code):
        active_consumers.remove(self)

    def receive(self, qset):
        # accepting data for this consumer
        self.send(text_data=json.dumps(qset))
    
