from django.contrib import admin
from .models import Post, Comment, Liked
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

#
# class UserAdmin(BaseUserAdmin):
#     list_display = ('name', 'email', 'phone')
#     search_fields = ('name', 'roll', 'email', 'phone', 'semester', 'registration')
#     filter_horizontal = ()
#     ordering = ['semester', 'name']
#     fieldsets = ()
#     readonly_fields = ()
#     list_filter = ('semester', 'is_active')
#
#     add_fieldsets = (
#         (None, {
#             'classes':'wide',
#             'fields': ('name', 'email', 'phone', 'semester', 'password1', 'password2'),
#         }),
#     )
#
#
# admin.site.register(User, UserAdmin)


class PostSearch(admin.ModelAdmin):
    search_fields = ('title', 'id', )


admin.site.register(Post, PostSearch)


admin.site.register(Comment)


admin.site.site_header = "CPI Admin"
admin.site.site_title = "CPI Admin Portal"
admin.site.index_title = "CPI Admin Panel"
