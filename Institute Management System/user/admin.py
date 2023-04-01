from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Profile , AuthCodes, StudentList
User = get_user_model()


admin.site.register(AuthCodes)


class UserAdmin(BaseUserAdmin):
    list_display = ('name', 'email', 'phone')
    search_fields = ('name', 'roll', 'email', 'phone', 'semester', 'registration')
    filter_horizontal = ()
    ordering = ['semester', 'name']
    fieldsets = ()
    readonly_fields = ()
    list_filter = ('semester', 'is_active')

    add_fieldsets = (
        (None, {
            'classes':'wide',
            'fields': ('name', 'email', 'phone',  'password1', 'password2'),
        }),
    )


class StudentListRoll(admin.ModelAdmin):
    list_filter = ('roll', 'registration')
    list_display = ('roll', 'registration')
    search_fields = ('roll', 'registration')
    filter_horizontal = ()
    ordering = ['roll', 'registration']


admin.site.register(StudentList, StudentListRoll)
admin.site.register(User, UserAdmin)
# Register your models here.
admin.site.register(Profile)