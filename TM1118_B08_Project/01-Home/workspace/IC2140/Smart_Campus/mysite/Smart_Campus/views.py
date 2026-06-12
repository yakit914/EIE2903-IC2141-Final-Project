from django.shortcuts import render
from . import iot_mqtt
from .models import Event
from django.http import JsonResponse
from django.core import serializers
from .forms import Time_DataForm
import json
from datetime import datetime, timedelta



def temp_data(request):
    events = Event.objects.all()
    if request.method == 'POST':
        form = Time_DataForm(request.POST)  
        if form.is_valid(): 
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')

            if start_date:
                events = events.filter(date_created__gte=start_date)

            if end_date:
                events = events.filter(date_created__lte=end_date)
    data = serializers.serialize('json', events)   
    data = json.dumps(data)
    return JsonResponse(data, safe=False) 

# Create your views here.
def index(request):
    events = Event.objects.order_by('-date_created') 
    context = {'events' : events} 
    return render(request, 'Smart_Campus/index.html',context)

def Log(request):
    form = Time_DataForm()
    List = Event.objects.order_by('-date_created')  

    if request.method == 'POST':
        form = Time_DataForm(request.POST)  
        if form.is_valid():  
        
            node_id = form.cleaned_data.get('node_id')
            loc = form.cleaned_data.get('loc')
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')
            temp_gt = form.cleaned_data.get('temp_gt')
            temp_lt = form.cleaned_data.get('temp_lt')
            hum_gt = form.cleaned_data.get('hum_gt')
            hum_lt = form.cleaned_data.get('hum_lt')
            light_gt = form.cleaned_data.get('light_gt')
            light_lt = form.cleaned_data.get('light_lt')
            snd_gt = form.cleaned_data.get('snd_gt')
            snd_lt = form.cleaned_data.get('snd_lt')


            if node_id and "All" not in node_id:
                List = List.filter(node_id__in=node_id)

            if loc and "All" not in loc:
                List = List.filter(loc__in=loc)

            if start_date:
                List = List.filter(date_created__gte=start_date)

            if end_date:
                List = List.filter(date_created__lte=end_date)

            if temp_gt:
                List = List.filter(temp__gte=temp_gt)

            if temp_lt:
                List = List.filter(temp__lte=temp_lt)

            if hum_gt:
                List = List.filter(hum__gte=hum_gt)

            if hum_lt:
                List = List.filter(hum__lte=hum_lt)

            if light_gt:
                List = List.filter(light__gte=light_gt)

            if light_lt:
                List = List.filter(light__lte=light_lt)

            if snd_gt:
                List = List.filter(snd__gte=snd_gt)

            if snd_lt:
                List = List.filter(snd__lte=snd_lt)
   
    context = {
        "form": form,
        "List": List, 
    }
    return render(request, 'Smart_Campus/Log.html', context)

def dashboard(request):
    events = Event.objects.order_by('date_created') 

    form = Time_DataForm()
    

    if request.method == 'POST':
        form = Time_DataForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')
            loc = form.cleaned_data.get('loc')
            node_id = form.cleaned_data.get('node_id')

            if start_date:
                events = events.filter(date_created__gte=start_date)

            if end_date:
                events = events.filter(date_created__lte=end_date)

    # Serialize the filtered events to JSON
    events_json = serializers.serialize('json', events)  

    print(events_json)          

    context = {
        'events_json': events_json,
        "form": form,
    }
    return render(request, 'Smart_Campus/dashboard.html', context)