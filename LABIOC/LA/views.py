from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.template import loader
from .models import SHHost

def index(request):
    all_sh_host = SHHost.objects.order_by('host_name')
    template = loader.get_template('LA/index.html')
    context = {
        'all_sh_host' : all_sh_host
    }
    return HttpResponse(template.render(context, request))

def showhost(request, owner_name):
    owner_sh_host = SHHost.objects.filter(owner = owner_name)
    context = { 'owner_sh_host': owner_sh_host }
    return render(request, 'LA/owner.html', {'owner_sh_host':owner_sh_host})

def showowner(request, host_name):
    sel_host = SHHost.objects.get(host_name = host_name)
    context = { 'sel_host' : sel_host }
    return render(request, 'LA/details.html', {'sel_host': sel_host})

