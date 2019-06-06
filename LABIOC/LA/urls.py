
from django.urls import include, path

from . import views

app_name = 'LA'
urlpatterns = [
    #path('', views.index, name='index'),
    path('', views.IndexView.as_view(), name = 'index'),
    path('owner/<str:owner_name>', views.showhost, name = 'owner'),
    path('host/<str:host_name>', views.showowner, name = 'detail'),
    path('hostlist', views.showhostlist, name = 'detailList'),
    path('shVM', views.showshVM, name = 'shVM'),
    path('redHost', views.showredHost, name ='redHost'),
    path('redVM', views.showredVM, name = 'redVM'),
]
