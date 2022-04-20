from django.db import models
from datetime import date
from django.contrib.auth.models import User

class Tweet(models.Model):
    tweetId = models.CharField(max_length=100)
    text = models.TextField(max_length=300)
    class Meta:
        unique_together = [('tweetId', 'text')]
    def __str__(self):
        return self.text
        
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField('Comment', max_length=250)
    date = models.DateField('comment date', default=date.today)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
    

