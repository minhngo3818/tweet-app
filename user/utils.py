from .models import Tweet
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage

def paginateTweets(request, tweets):
    pagination = Paginator(tweets, 4)
    page = request.GET.get('tweets')
    pagin_tweets = pagination.get_page(page)

    return pagin_tweet

