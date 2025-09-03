from django.db import models
from django.utils import timezone

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField()
    counted_view = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title
# Create your models here.
class Ticket(models.Model):
    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField()