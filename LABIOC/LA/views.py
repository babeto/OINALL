from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.template import loader
from .models import SHHost
from .models import SHVirtualMachine
from .models import REDHost
from .models import REDVirtualMachine
from .models import AzureVirtualMachine
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

'''
def index(request):
    all_sh_host = SHHost.objects.all() #.order_by('machine_name')
    template = loader.get_template('LA/index.html')
    context = {
        'all_sh_host' : all_sh_host
    }
    return HttpResponse(template.render(context, request))
'''

class IndexView(generic.ListView):
    template_name = 'LA/index.html'
    context_object_name = 'all_sh_host'
    def get_queryset(self):
        """return all the Shanghai host"""
        return SHHost.objects.filter(obsolete = False).order_by('compliant')

def showhost(request, owner_name):
    owner_sh_host = SHHost.objects.filter(owner = owner_name)
    context = { 'owner_sh_host': owner_sh_host }
    return render(request, 'LA/owner.html', {'owner_sh_host':owner_sh_host})

def showowner(request, machine_name):
    sel_host = SHHost.objects.get(machine_name = machine_name)
    context = { 'sel_host' : sel_host }
    return render(request, 'LA/details.html', {'sel_host': sel_host})

def showhostlist(request):
    if request.method=="POST":
        hostlist = request.POST.getlist('machine_name')
        host_list=[]
        for host in hostlist:
            host_list.append(SHHost.objects.get(machine_name=host))
        context = {'host_list': host_list }
        return render(request, 'LA/detailList.html', context)

def showshVM(request):
    shVM = SHVirtualMachine.objects.defer("installedupdate").order_by('compliant')
    context = {'shVM':shVM}
    return render(request, 'LA/SHVM.html', context)

def showredVM(request):
    redVM = REDVirtualMachine.objects.all().order_by('compliant')
    context = {'redVM':redVM}
    return render(request, 'LA/REDVM.html', context)

def showredHost(request):
    redHost = REDHost.objects.filter(obsolete = False).order_by('compliant')
    context = {'redHost':redHost}
    return render(request, 'LA/REDHost.html', context)

def showazureVM(request):
    azureVM = AzureVirtualMachine.objects.all().order_by('resourcegroupname')
    context = {'azureVM' : azureVM}
    return render(request, 'LA/AzureVM.html', context)

def show_shhost_details(request, machine_name):
    machine = SHHost.objects.get(machine_name = machine_name)
    context = {'machine' : machine}
    return render(request, 'LA/details.html', context)

def show_shvm_details(request, machine_name):
    machine = SHVirtualMachine.objects.get(machine_name = machine_name)
    context = {'machine' : machine}
    return render(request, 'LA/details.html', context)

def show_redhost_details(request, machine_name):
    machine = REDHost.objects.get(machine_name = machine_name)
    context = {'machine' : machine}
    return render(request, 'LA/details.html', context)

def show_redvm_details(request, machine_name):
    machine = REDVirtualMachine.objects.get(machine_name = machine_name)
    context = {'machine' : machine}
    return render(request, 'LA/details.html', context)



