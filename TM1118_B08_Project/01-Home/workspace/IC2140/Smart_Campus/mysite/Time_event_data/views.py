from django.shortcuts import render
from .forms import Time_DataForm, Venue_Form
from .models import Venue
from Smart_Campus.models import Event
from django.db.models import Avg, Max, Min

def index(request):
    form = Time_DataForm()
    venue_form = Venue_Form()
    List = []
    Buttons = []
    Data_list = []
    Each_Venue_Data = []
    OVERALL_DATA = []
    OVERALL = []
    
    if request.method == 'POST':
         
        form = Time_DataForm(request.POST)  
        if form.is_valid():  
            
            
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

            if len(loc) > 0:
                List =  Venue.objects.all()
                EVENT_list = Event.objects.all()

            if loc:
                List = List.filter(Venue__in=loc)
                VENT_list = EVENT_list.filter(loc__in=loc)
            
            if start_date and end_date:
                List = List.filter(Time_start__lt=end_date, Time_end__gt=start_date)
         
            

            
            for i in range(len(List)):
                Ven_Form = Venue_Form(initial={'start_date': List[i].Time_start, 'end_date': List[i].Time_end,'Venue': List[i].Venue})
                Event_each_venue = Event.objects.order_by('-date_created') 
                Event_each_venue = Event_each_venue.filter(date_created__gte=List[i].Time_start).filter(date_created__lte=List[i].Time_end).filter(loc=List[i].Venue)
                #Event_each_venue = Event_each_venue.filter(date_created__gte=start_date).filter(date_created__lte=end_date)

                if temp_gt:
                    Event_each_venue = Event_each_venue.filter(temp__gte=temp_gt)

                if temp_lt:
                    Event_each_venue = Event_each_venue.filter(temp__lte=temp_lt)

                if hum_gt:
                    Event_each_venue = Event_each_venue.filter(hum__gte=hum_gt)

                if hum_lt:
                    Event_each_venue = Event_each_venue.filter(hum__lte=hum_lt)

                if light_gt:
                    Event_each_venue = Event_each_venue.filter(light__gte=light_gt)

                if light_lt:
                    Event_each_venue = Event_each_venue.filter(light__lte=light_lt)

                if snd_gt:
                    Event_each_venue = Event_each_venue.filter(snd__gte=snd_gt)

                if snd_lt:
                    Event_each_venue = Event_each_venue.filter(snd__lte=snd_lt)

                Buttons.append(Ven_Form)
                if len(Event_each_venue) > 0:
                    Data = Event_each_venue.values('loc').aggregate(Avg("temp"),Max("temp"),Min("temp"),Avg("hum"),Max("hum"),Min("hum"),Avg("light"),Max("light"),Min("light"),Avg("snd"),Max("snd"),Min("snd"))
                    for key in Data:
                        if Data[key] is not None:  
                            Data[key] = format(Data[key], '.2f')
                    OVERALL_DATA.extend(Event_each_venue)
                    Each_Venue_Data.append(Data)
                    

            OVERALL = Event.objects.filter(id__in=[event.id for event in OVERALL_DATA]).aggregate(
                Avg("temp"), Max("temp"), Min("temp"),
                Avg("hum"), Max("hum"), Min("hum"),
                Avg("light"), Max("light"), Min("light"),
                Avg("snd"), Max("snd"), Min("snd")
            )

            for key in OVERALL:
                if OVERALL[key] is not None: 
                    OVERALL[key] = format(OVERALL[key], '.2f')
                    


        Each_Venue_Data = zip(List, Each_Venue_Data)
        List = zip(List, Buttons)
        
        Data_list = []
        
        # venue_form = Venue_Form(request.POST)
        # if venue_form.is_valid():
        #     start_date_V = venue_form.cleaned_data.get('start_date')
        #     end_date_V = venue_form.cleaned_data.get('end_date')
        #     data_venue_V = venue_form.cleaned_data.get('Venue')

        #     if start_date_V:
        #         Data_list = Event.objects.all()
        #     if start_date_V:
        #         Data_list = Data_list.filter(date_created__gte=start_date_V)
        #     if end_date_V:
        #         Data_list = Data_list.filter(date_created__lte=end_date_V)
        #     if data_venue_V:
        #         Data_list = Data_list.filter(loc=data_venue_V)

                
            
              
            
    context = {
        "form": form,
        "List": List,
        "Data_list": Data_list,
        "Each_Venue_Data":Each_Venue_Data,
        "OVERALL":OVERALL,
    }
    return render(request, 'Time_event_data/index.html', context)



