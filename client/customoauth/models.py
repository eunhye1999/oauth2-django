from django.db import models
from django.contrib.auth.models import User

class Providers(models.Model):

    name = models.CharField(max_length=50)
    url = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Social_applications(models.Model):
    provider = models.ForeignKey(Providers, on_delete=models.CASCADE)

    name = models.CharField(max_length=50)
    client_id = models.CharField(max_length=200)
    client_secret = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Social_token(models.Model):
    application = models.ForeignKey(Social_applications, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    token = models.CharField(max_length=200)
    expire = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.application
    
class Social_account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    provider = models.ForeignKey(Providers, on_delete=models.CASCADE)

    uid = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user