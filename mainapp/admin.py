from django.contrib import admin
from mainapp.models import Clients, Companys

class ClientsAdmin(admin.ModelAdmin):

    list_display = ('name', 'company', 'email', 'phone', 'interests')
    search_fields = ('name', 'company__name', 'email', 'phone', 'interests')

class CompanysAdmin(admin.ModelAdmin):

    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Clients, ClientsAdmin)
admin.site.register(Companys, CompanysAdmin)