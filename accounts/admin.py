from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Accounts


# class AccountAdmin(UserAdmin):
#     list_display = ['email', 'first_name', 'last_name', 'mobile']
#     list_filter = ()
#     search_fields = ('mobile', 'email')
#     readonly_fields = ('first_name', 'last_name', 'last_login', 'date_joined')
#     fieldsets = ()
#     filter_horizontal = ()


admin.site.register(Accounts)
