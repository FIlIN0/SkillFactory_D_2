from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import PostFilter
from .forms import PostForm


class NewsList(ListView):
    model = Post
    template_name = 'flatpages/news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-id')
    paginate_by = 1


class SearchList(ListView):
    model = Post
    template_name = 'flatpages/search.html'
    context_object_name = 'search'
    queryset = Post.objects.order_by('-id')
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())  # вписываем фильтр в контекст
        return context


class NewDetail(DetailView):
    model = Post
    template_name = 'flatpages/new.html'
    context_object_name = 'new'


class AddPost(CreateView):
    template_name = 'flatpages/add.html'
    form_class = PostForm  # добавляем форм класс, чтобы получать доступ к форме через метод POST


class PostUpdateView(UpdateView):
    template_name = 'flatpages/add.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(DeleteView):
    template_name = 'flatpages/delete.html'
    queryset = Post.objects.all()
    context_object_name = 'new'
    success_url = '/news/'