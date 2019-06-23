from django.urls import path

from . import views

app_name = 'customoauth'

urlpatterns = [
    path('token/', views.accessToken, name='token')
]