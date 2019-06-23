from django.urls import path

from . import views

app_name = 'oauth2access'

urlpatterns = [
    path('authorize/', views.authorize, name='authorize'),
    path('token/', views.token, name='token'),
    path('info/', views.infomation, name='info')
]

