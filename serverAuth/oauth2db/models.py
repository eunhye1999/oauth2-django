from django.db import models
from django.contrib.auth.models import User


class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=50)
    client_id = models.CharField(max_length=100)
    client_secret = models.CharField(max_length=200)
    redirect_uri = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Accesstgrant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    application = models.ForeignKey(Application, on_delete=models.CASCADE)

    code = models.CharField(max_length=100)
    expires = models.DateTimeField()
    redirect_uri = models.CharField(max_length=200)
    scope = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code


class Accesstoken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    application = models.ForeignKey(Application, on_delete=models.CASCADE)

    token = models.CharField(max_length=50)
    expires = models.DateTimeField()
    scope = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user
