
from django.urls import include, path

from . import views

app_name = 'LA'
urlpatterns = [
    #path('', views.index, name='index'),
    path('', views.IndexView.as_view(), name = 'index'),
    path('owner/<str:owner_name>', views.showhost, name = 'owner'),
    path('host/<str:machine_name>', views.showowner, name = 'detail'),
    path('hostlist', views.showhostlist, name = 'detailList'),
    path('shVM', views.showshVM, name = 'shVM'),
    path('redHost', views.showredHost, name ='redHost'),
    path('redVM', views.showredVM, name = 'redVM'),
    path('azureVM', views.showazureVM,name = 'azureVM'),
    path('shHost/details/<str:machine_name>', views.show_shhost_details, name = 'details_shhost'),
    path('shVM/details/<str:machine_name>', views.show_shvm_details, name = 'details_shvm'),
    path('redHost/details/<str:machine_name>', views.show_redhost_details, name = 'details_redhost'),
    path('redVM/details/<str:machine_name>', views.show_redvm_details, name = 'details_redvm'),
]
