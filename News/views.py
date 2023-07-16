from django.core.cache import cache
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import resolve

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category
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
    queryset = Post.objects.order_by('-time_post')
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())  # вписываем фильтр в контекст
        return context


class NewDetail(DetailView):
    model = Post
    template_name = 'flatpages/new.html'
    context_object_name = 'new'
    queryset = Post.objects.all()

    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта, как ни странно
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)

        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)

        return obj


class AddPost(PermissionRequiredMixin, CreateView):
    permission_required = ('News.add_post',)
    template_name = 'flatpages/add.html'
    form_class = PostForm  # добавляем форм класс, чтобы получать доступ к форме через метод POST


class PostUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('News.change_post',)
    #   login_url = '/news/'
    template_name = 'flatpages/add.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('News.delete_post',)
    template_name = 'flatpages/delete.html'
    queryset = Post.objects.all()
    context_object_name = 'new'
    success_url = '/news/'


class PostCategoryView(ListView):
    model = Post
    template_name = 'flatpages/category.html'
    context_object_name = 'news'
    ordering = ['-id']
    paginate_by = 3

    def get_queryset(self):
        self.id = resolve(self.request.path_info).kwargs['pk']
        c = Category.objects.get(id=self.id)
        queryset = Post.objects.filter(categories=c)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        category = Category.objects.get(id=self.id)
        is_subscribed = category.subscribers.filter(id=user.id)
        if not user.is_authenticated:
            redirect('http://127.0.0.1:8000/accounts/login/')
        else:
            context['category'] = category
            if is_subscribed:
                context['is_subscribed'] = is_subscribed
            return context


@login_required
def subscribe_to_category(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)

    if not category.subscribers.filter(id=user.id).exists():
        category.subscribers.add(user)
        email = user.email
        html = render_to_string(
            'flatpages/mail/subscribed.html',
            {
                'category': category,
                'user': user
            },
        )

        msg = EmailMultiAlternatives(
            subject=f'{category} subscription',
            body='Yes',
            from_email='tani4400@yandex.ru',
            to=[email, ],
        )

        msg.attach_alternative(html, 'text/html')

        try:
            msg.send()
        except Exception as e:
            print(e)
        print('Successes')
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def unsubscribe_from_category(request, pk):
    user = request.user
    c = Category.objects.get(id=pk)
    if c.subscribers.filter(id=user.id).exists():
        c.subscribers.remove(user)
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def make_me_author(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/news/')

def index (request):
    return redirect('/news/')
