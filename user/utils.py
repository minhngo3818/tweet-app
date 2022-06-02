from .models import Tweet
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def paginateTweets(request, tweets, results):
    pass