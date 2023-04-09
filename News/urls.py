from django.urls import path
from .views import NewsList, NewDetail, SearchList, AddPost, PostDeleteView, PostUpdateView, make_me_author, \
    PostCategoryView, subscribe_to_category, unsubscribe_from_category, index

urlpatterns = [

    path('', NewsList.as_view(), name='news'),
    path('<int:pk>', NewDetail.as_view(), name='new'),
    path('delete/<int:pk>', PostDeleteView.as_view(), name='delete'),
    path('search/', SearchList.as_view()),
    path('add/', AddPost.as_view(), name='add'),
    path('update/<int:pk>', PostUpdateView.as_view(), name='post_update'),
    path('upgrade/', make_me_author, name='upgrade1'),
    path('category/<int:pk>', PostCategoryView.as_view(), name='category'),
    path('subscribed/<int:pk>', subscribe_to_category, name='subscribe'),
    path('unsubscrib/<int:pk>', unsubscribe_from_category, name='unsubscribe'),
    path('profile/', index, name='profile'),


]