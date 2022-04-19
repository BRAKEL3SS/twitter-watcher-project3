from django.contrib import admin
from .models import Comment, Tweet
# Register your models here.

admin.site.register(Comment)
admin.site.register(Tweet)