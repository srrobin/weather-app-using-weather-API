from django.shortcuts import render,redirect
import requests
from.models import City
from .forms import CityForm

def weather_list(request):
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=60836f26d9c3044fcd2d293b764575b9"


    err_msg = ''
    message = ''
    message_class = ''

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            city_count = City.objects.filter(name=new_city).count()
            if city_count == 0:
                data = requests.get(url.format(new_city)).json()
                if data['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'City does not exist in the world!'
            else:
                err_msg = 'City already exists in the database!'

        if err_msg:
            message = err_msg
            message_class = 'alert alert-danger'
        else:
            message = 'City added successfully!'
            message_class = 'alert alert-success'


    form = CityForm()



    cities = City.objects.all()
    weather_data = []
    for city in reversed(cities):
        data = requests.get(url.format(city)).json()
        city_weather = {
            'city': city.name,
            'temp': data['main']['temp'],
            'des' : data['weather'][0]['description'],
            'icon': data['weather'][0]['icon']
        }
        weather_data.append(city_weather)

    context = {
        'weather_data': weather_data,
        'form':form ,
        'message': message,
        'message_class': message_class
    }
    return render(request,'index.html',context)


def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()

    return redirect('home')