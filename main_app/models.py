from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

# Create your models here.

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=250)
    date = models.DateField('comment date')

    def __str__(self):
        return self.text
    
    # def get_absolute_url(self):
    #     return reverse('detail', kwargs={'comment_id': self.id})
