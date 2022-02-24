from django.urls import path
from . import views
from main.views import get_info, get_info_by_num, get_types, get_elem, get_sign

urlpatterns = [
    path('', views.index, name='main'),
    path('type/', views.get_types),
    path('type/<str:element>', get_elem, name="type"),
    path('<int:month>/<int:day>', get_sign),
    path('<int:zodiac_num>', get_info_by_num),
    path('<str:zodiac_name>', get_info, name='horoskop'),
]
