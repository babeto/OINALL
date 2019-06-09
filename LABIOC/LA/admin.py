from django.contrib import admin

# Register your models here.

from .models import SHHost
from .models import SHVirtualMachine
from .models import REDHost
from .models import REDVirtualMachine


admin.site.register(SHHost)
admin.site.register(SHVirtualMachine)
admin.site.register(REDHost)
admin.site.register(REDVirtualMachine)
