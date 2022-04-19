from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('feed/', views.feed, name='feed'),
    path('feed/<str:trend>', views.trend, name='trend'),
    path('feed/<str:trend>/<int:tweet_id>', views.tweet, name='tweet'),
    path('feed/<str:trend>/<int:tweet_id>/add_comment', views.add_comment, name='add_comment'),
    path('feed/<str:trend>/<int:tweet_id>/<int:pk>/update', views.CommentUpdate.as_view(), name='update_comment'),
    path('feed/<str:trend>/<int:tweet_id>/<int:pk>/delete', views.CommentDelete.as_view(), name='delete_comment')
]