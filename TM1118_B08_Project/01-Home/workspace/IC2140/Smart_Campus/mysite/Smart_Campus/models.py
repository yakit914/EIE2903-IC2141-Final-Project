from django.db import models

# Create your models here.
class Event(models.Model):
    #Fields
    node_id = models.CharField(max_length=6,blank = False)
    loc = models.CharField(max_length=10,blank = False)
    temp = models.DecimalField(max_digits=4, decimal_places=1,blank = False)
    hum = models.DecimalField(max_digits=4, decimal_places=1,blank = False)
    light = models.IntegerField(blank = False)
    snd = models.IntegerField(blank = False)
    date_created = models.DateTimeField(auto_now_add=True)
    #Methods
    def __str__(self):
        return 'Event #{}'.format(self.id)