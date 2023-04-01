from django.contrib import admin

from .models import SemesterSystem, SemesterSystemInfo, RegistrationFee, MidTermFee

admin.site.register(RegistrationFee)
admin.site.register(MidTermFee)
admin.site.register(SemesterSystem)
admin.site.register(SemesterSystemInfo)
# Register your models here.
