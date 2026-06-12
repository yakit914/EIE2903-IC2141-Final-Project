from django.db import models

# Create your models here.
class Time_Event(models.Model):
    #Fields
    node_id = models.CharField(max_length=6,blank = False)
    loc = models.CharField(max_length=10,blank = False)
    Description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=False)
    #Methods
    def __str__(self):
        return 'Time Event #{}'.format(self.id)

    start_date = models.DateTimeField(auto_now_add=False,blank = False)


    
    end_date = models.DateTimeField(auto_now_add=False,blank = False)

class Venue(models.Model):
    Venue = models.CharField(max_length=10,blank = False)
    Time_start = models.DateTimeField(auto_now_add=False,blank = False)
    Time_end = models.DateTimeField(auto_now_add=False,blank = False)
    Event = models.CharField(max_length=10,blank = False)
    Instructor  = models.CharField(max_length=20,blank = False)
    
    def __str__(self):
        return 'Venue Event #{}'.format(self.id)