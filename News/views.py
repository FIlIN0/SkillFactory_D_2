from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group


class NewsList(ListView):
    model = Post
    template_name = 'flatpages/news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-id')
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


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


class AddPost(PermissionRequiredMixin, CreateView):
    permission_required = ('News.add_post', )
    template_name = 'flatpages/add.html'
    form_class = PostForm  # добавляем форм класс, чтобы получать доступ к форме через метод POST


class PostUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('News.change_post', )
    #   login_url = '/news/'
    template_name = 'flatpages/add.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('News.delete_post', )
    template_name = 'flatpages/delete.html'
    queryset = Post.objects.all()
    context_object_name = 'new'
    success_url = '/news/'



@login_required
def make_me_author(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/news/')
