import django_filters
from django_filters import FilterSet
from django_filters.widgets import RangeWidget

from .models import Post


# создаём фильтр
class PostFilter(FilterSet):
    time_post = django_filters.DateFromToRangeFilter(widget=RangeWidget(attrs={'type': 'date'}))

    class Meta:
        model = Post
        fields = {'name': ['icontains'],
                  'authors': ['exact'],
                  }
