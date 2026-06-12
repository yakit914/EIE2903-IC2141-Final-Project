from django.forms import ModelForm, DateInput
from .models import Event
from django import forms
from django.db.models import Sum
class Time_DataForm(forms.Form):
    
    start_date = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label="Start Date"
    )
    end_date = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label="End Date"
    )

    loc_list = Event.objects.values('loc').annotate(Total=Sum('loc'))
    loc_choice = [("All","All")]
    for i in loc_list:
        add = i["loc"]
        loc_choice.append((str(add),str(add)))

    loc = forms.MultipleChoiceField(
        required=False,
        choices= loc_choice,
        label="Location",  
    )

    node_id_list = Event.objects.values('node_id').annotate(Total=Sum('node_id'))
    node_id_choice = [("All","All")]
    for i in node_id_list:
        add = i["node_id"]
        node_id_choice.append((str(add),str(add)))

    node_id = forms.MultipleChoiceField(
        required=False,
        choices=node_id_choice,
        label="Node_ID",  
    )

    temp_gt = forms.DecimalField(
        max_digits=4,
         decimal_places=1,
        required=False, 
    )
    temp_lt = forms.DecimalField(
        max_digits=4,
         decimal_places=1,
        required=False, 
    )

    hum_gt = forms.DecimalField(
        max_digits=4,
         decimal_places=1,
        required=False, 
    )
    hum_lt = forms.DecimalField(
        max_digits=4,
         decimal_places=1,
        required=False, 
    )

    light_gt = forms.IntegerField(required=False)
    light_lt = forms.IntegerField(required=False)

    snd_gt = forms.IntegerField(required=False)
    snd_lt = forms.IntegerField(required=False)





