from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post


class NewsList(ListView):
    model = Post
    template_name = 'flatpages/news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-id')


class NewDetail(DetailView):
    model = Post
    template_name = 'flatpages/new.html'
    context_object_name = 'new'
# Create your views here.
