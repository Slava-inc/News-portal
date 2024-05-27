from django_filters import FilterSet, DateFilter, DateFromToRangeFilter
from .models import Post
from django_filters.widgets import RangeWidget, DateRangeWidget

# Создаем свой набор фильтров для модели Post
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class PostFilter(FilterSet):
    # time_in = DateFilter(lookup_expr='range', widget=DateRangeWidget())
    time_in = DateFromToRangeFilter(label='Creation date', widget=RangeWidget(attrs={'type': 'date'}))

    class Meta:
       # В Meta классе мы должны указать Django модель,
       # в которой будем фильтровать записи.
       model = Post
       # В fields мы описываем по каким полям модели
       # будет производиться фильтрация.
       fields = {
           # поиск по названию
           'header': ['icontains'],
           # по имени автора
           'author': ['exact'],
           # 'time_in': ['lt', 'gt'],  # дата должна быть в интервале
       }