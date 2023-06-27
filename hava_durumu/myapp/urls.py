from django.urls import path

# internals
from . import views

urlpatterns = [
    path('', views.index, name="app-index"),
]
