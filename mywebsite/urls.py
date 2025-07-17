from django.urls import path
from mywebsite import views

app_name = 'mywebsite'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('<int:book_id>/', views.detail, name='detail'),
]