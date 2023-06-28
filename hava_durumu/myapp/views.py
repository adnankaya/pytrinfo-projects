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
        return JsonResponse([data_dict], safe=False)
    # eger all parametresi client tarafindan gonderilmisse butun kayitlari cevap olarak döndür
    all = request.GET.get("all")
    if all:
        weathers = Weather.objects.all()
        serialized_data = [
            {
                "id": obj.id,
                "city": obj.city,
                "icon": obj.icon,
                "temperature": obj.temperature,
                "description": obj.description,
                "updated_date": obj.updated_date.strftime('%Y-%m-%d %H:%M')
            }
            for obj in weathers
        ]
        return JsonResponse(serialized_data, safe=False)

    return render(request, "myapp/index.html")
