from django.urls import path
from mywebsite import views1

app_name = 'mywebsite'

urlpatterns = [
    path('', views1.index, name='index'),
    path('about/', views1.about, name='about'),
    path('<int:book_id>/', views1.detail, name='detail'),
]