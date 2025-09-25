from django.contrib import admin

# Register your models here.
from home.models import Azienda,UsersAzienda

class AziendaAdmin(admin.ModelAdmin):
    pass

class UsersAziendaAdmin(admin.ModelAdmin):
    pass
admin.site.register(UsersAzienda,UsersAziendaAdmin)
admin.site.register(Azienda, AziendaAdmin)