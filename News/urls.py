from django.urls import path
from .views import NewsList, NewDetail, SearchList, AddPost, PostDeleteView, PostUpdateView
urlpatterns = [

    path('', NewsList.as_view()),
    path('<int:pk>', NewDetail.as_view(), name='new'),
    path('delete/<int:pk>', PostDeleteView.as_view(), name='delete'),
    path('search/', SearchList.as_view()),
    path('add/', AddPost.as_view(), name='add'),
    path('update/<int:pk>', PostUpdateView.as_view(), name='post_update'),
]