from django.shortcuts import render
from django.http.response import JsonResponse # yeni
# internals
from .utils import request_to_weatherapi # yeni
from .models import Weather

def index(request):
    city = request.GET.get("city")
    if city:
        data_dict = request_to_weatherapi(city)
        qset = Weather.objects.filter(city__iexact=city)
        if qset.exists():
            qset.update(**data_dict)
        else:
            new_weather = Weather.objects.create(**data_dict)
        return JsonResponse(data_dict)

    return render(request, "myapp/index.html")
