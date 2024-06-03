from django.db import models
from django.conf import settings


# Create your models here.
class EventInfo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    event_name = models.CharField(max_length=250)
    event_type = models.CharField(max_length=50)
    event_date = models.DateField()
    event_location= models.CharField(max_length=100)
    event_description = models.TextField()
    event_reg_deadline = models.DateTimeField()
    event_max_capacity = models.IntegerField()
    event_image = models.ImageField(upload_to='event_images/',blank=True,null=True,default='default.jpg')
    created_at = models.DateTimeField(auto_now_add=True)
    event_entry_fee = models.IntegerField(blank=True,null=True,default=-1)


    def __str__(self):
        return self.event_name


class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    event = models.ForeignKey(EventInfo, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} booked {self.event.event_name}"