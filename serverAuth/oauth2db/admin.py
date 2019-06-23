from django.contrib import admin
from oauth2db.models import  Application, Accesstgrant, Accesstoken

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name','user', 'client_id','redirect_uri']
admin.site.register(Application, ApplicationAdmin)

class AccesstgrantAdmin(admin.ModelAdmin):
    list_display = ['id', 'user','application', 'code', 'scope','redirect_uri','expires']
admin.site.register(Accesstgrant, AccesstgrantAdmin)

class AccesstokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'application','token','scope','expires']
admin.site.register(Accesstoken, AccesstokenAdmin)
