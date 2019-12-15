from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.weather_list, name = 'home'),
    path('delete/<city_name>/',views.delete_city, name = 'delete_city')
]
