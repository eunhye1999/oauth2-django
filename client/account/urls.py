from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
    path('login/', views.login, name="login"),

    path('profile/', views.profile, name="profile"),

    path('<str:provider>/login/', views.redirect_login, name='provider_redirect'),
    path('<str:provider>/login/callback/', views.redirect_callback, name='provider_redirect_callback'),
]
