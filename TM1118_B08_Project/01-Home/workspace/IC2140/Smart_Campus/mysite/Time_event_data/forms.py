from django.forms import ModelForm, DateInput
from .models import Venue
from django import forms
from django.db.models import Sum

class Time_DataForm(forms.Form):

    loc_list = Venue.objects.values('Venue').annotate(Total=Sum('Venue'))
    loc_choice = []
    for i in loc_list:
        add = i["Venue"]
        loc_choice.append((str(add),str(add)))

    loc = forms.MultipleChoiceField(
        required=False,
        choices= loc_choice,
        label="Location",
        #only one
    )

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


    

class Venue_Form(forms.Form):
    start_date_V = forms.DateTimeField(
        required=False,
        widget=forms.HiddenInput(),
        label="Start Date"

    )
    end_date_V = forms.DateTimeField(
        required=False,
        widget=forms.HiddenInput(),
        label="End Date"

        
    )

    Venue_V = forms.CharField(required=False,label="Venue",widget=forms.HiddenInput() )
    
    