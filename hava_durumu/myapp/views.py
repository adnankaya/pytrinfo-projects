from django.shortcuts import render
from django.http.response import JsonResponse
# internals
from .utils import request_to_weatherapi
from .models import Weather
from .consumers import active_consumers

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
    # websocket ile haberleşme yapmak için view üzerinden tetikleme yapacagiz
    triggered = request.GET.get("trigger")
    deleted_city = request.GET.get("deleted_city")
    if triggered and deleted_city:
        # silinecek objeyi bul
        obj = Weather.objects.filter(city__iexact=deleted_city)
        if obj.exists():
            obj.delete()
        # butun kayitlari getir
        qset = Weather.objects.all()
        # serialize ederek consumer'a gondermemiz gerekiyor.
        qs_weathers = [
            {
                "id": obj.id,
                "city": obj.city,
                "icon": obj.icon,
                "temperature": obj.temperature,
                "description": obj.description,
                "updated_date": obj.updated_date.strftime('%Y-%m-%d %H:%M')
            }
            for obj in qset
        ]
        for consumer in active_consumers:
            consumer.receive(qset=qs_weathers)
        return JsonResponse({"message":"Tetiklendi!"}, safe=False)

    return render(request, "myapp/index.html")
