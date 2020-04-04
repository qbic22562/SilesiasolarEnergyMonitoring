from django.urls import path, include
from .api import LocationAPI, MeterAPI, NodeAPI

urlpatterns = [
    path('locations', LocationAPI.as_view()),
    path('meters', MeterAPI.as_view()),
    path('nodes', NodeAPI.as_view())



    # path('meter', MeterAPI.as_view()),
    # path('node', NodeAPI.as_view()),
]