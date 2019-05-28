"""
Definition of urls for LABIOC.
"""

from django.urls import include, path

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', LABIOC.views.home, name='home'),
    # url(r'^LABIOC/', include('LABIOC.LABIOC.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    path('LA/',include('LA.urls')),
    path('admin/', admin.site.urls),
]
