from django.shortcuts import render, redirect
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from .models import Tweet
from.models import Comment
from .forms import CommentForm
import tweepy
import os

def home(request):
    return render(request, 'home.html')

def feed(request):
  consumer_key = os.environ["consumer_key"]
  consumer_secret = os.environ["consumer_secret"]
  access_token = os.environ["access_token"]
  access_token_secret = os.environ["access_token_secret"]
  auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token, access_token_secret)
  api = tweepy.API(auth)
  woeid=23424977
  trendslist = api.get_place_trends(id = woeid)
  trends = trendslist[0]['trends']

  return render(request, 'feed.html', {'trends': trends })

def signup(request):
  error_message = ''
  if request.method =='POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('feed')
    else:
        error_message = 'Invalid Sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render (request, 'registration/signup.html', context)    

def trend(request, trend):
  bearerToken = os.environ["bearer_token"]
  client = tweepy.Client(bearer_token=bearerToken)
  query = trend
  tweets = client.search_recent_tweets(query=query)
  return render(request, 'trend.html', { 'trend': trend, 'tweets':tweets })

def tweet(request, trend, tweet_id):
  bearerToken = os.environ["bearer_token"]
  client = tweepy.Client(bearer_token=bearerToken)
  ids = tweet_id
  tweets = client.get_tweets(ids=ids)
  print(tweets.data)
  text = tweets.data[0]
  if not Tweet.objects.filter(tweetId=tweet_id, text=text):
    tweetData = Tweet(tweetId=tweet_id, text=text)
    tweetData.save()
  comment_form = CommentForm()
  tId = Tweet.objects.filter(tweetId=tweet_id).values('id')
  comment = Comment.objects.filter(tweet_id=tId[0]['id'])
  return render(request, 'tweet.html', { 'tweet_id': tweet_id, 'trend': trend, 'tweets': tweets , 'comment_form': comment_form, 'comments': comment })

@login_required
def add_comment(request, trend, tweet_id):
    form = CommentForm(request.POST)
    if form.is_valid():
      new_comment = form.save(commit=False)
      new_comment.user = request.user
      new_comment.tweet = Tweet.objects.get(tweetId=tweet_id)
      new_comment.save()
    return redirect('tweet', trend=trend, tweet_id=tweet_id)

class CommentUpdate(LoginRequiredMixin, UpdateView):
  model = Comment
  fields = ['text']
  def get_success_url(self):
      trend = self.kwargs['trend']
      tweet_id = self.kwargs['tweet_id']
      return reverse("tweet", kwargs={'trend': trend, 'tweet_id': tweet_id})

class CommentDelete(LoginRequiredMixin, DeleteView):
  model = Comment
  def get_success_url(self):
    trend = self.kwargs['trend']
    tweet_id = self.kwargs['tweet_id']
    return reverse("tweet", kwargs={'trend': trend, 'tweet_id': tweet_id})
  