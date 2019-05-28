
from django.urls import include, path

from . import views

app_name = 'LA'
urlpatterns = [
    path('', views.index, name='index'),
    path('owner/<str:owner_name>', views.showhost, name = 'owner'),
    path('host/<str:host_name>', views.showowner, name = 'detail'),

]
