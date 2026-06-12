from django.shortcuts import render
from Smart_Campus.models import Event
import datetime
from django.utils.timesince import timesince
from django.db.models import Q

# Create your views here.
def index(request):


    Abnormal_events = Event.objects.order_by('-date_created') # date_created descending order
    Abnormal_events = Abnormal_events.filter(
    Q(date_created__hour__gte=23) | Q(date_created__hour__lte=6))
    Abnormal_events_temp = Abnormal_events.filter(Q(temp__gte = 30) | Q(temp__lte = 10))
    Abnormal_events_light = Abnormal_events.filter(light__gte = 30)
    Abnormal_events_snd = Abnormal_events.filter(snd__gte = 65)

    temp_time = []
    light_time = []
    snd_time = []

    

    for event in Abnormal_events_temp:
        temp_time.append(timesince(event.date_created))

    for event in Abnormal_events_light:
        light_time.append(timesince(event.date_created))

    for event in Abnormal_events_snd:
        snd_time.append(timesince(event.date_created))
    
    Abnormal_events_temp = zip(Abnormal_events_temp,temp_time)
    Abnormal_events_light = zip(Abnormal_events_light,light_time)
    Abnormal_events_snd = zip(Abnormal_events_snd,snd_time)
    
    context = {'Abnormal_events':{'temp':Abnormal_events_temp,
               'light': Abnormal_events_light,
               'snd' : Abnormal_events_snd,}
            }


    return render(request, 'Data_analysis/index.html',context)