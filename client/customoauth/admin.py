from django.contrib import admin
from customoauth.models import  Providers, Social_applications, Social_token, Social_account

class ProvidersAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
admin.site.register(Providers, ProvidersAdmin)

class Social_applicationsAdmin(admin.ModelAdmin):
    list_display = ['id', 'provider', 'client_id']
admin.site.register(Social_applications, Social_applicationsAdmin)

class Social_tokenAdmin(admin.ModelAdmin):
    list_display = ['id', 'application','user']
admin.site.register(Social_token, Social_tokenAdmin)

class Social_accountAdmin(admin.ModelAdmin):
    list_display = ['id', 'provider','user', 'uid']
admin.site.register(Social_account, Social_accountAdmin)