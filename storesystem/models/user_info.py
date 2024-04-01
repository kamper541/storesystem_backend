from django.db import models
from django.contrib.auth import authenticate, get_user_model
User = get_user_model()

class UserInfo(models.Model):
    instance_id = models.CharField(max_length=255, primary_key=True)
    user = models.ForeignKey(User,to_field='username', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True)
    verified = models.BooleanField(default=False)
    status = models.TextField()
    email = models.EmailField(blank=True, null=True, default=None)
    address = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    zip = models.CharField(max_length=255, blank=True, null=True)
    country = models.JSONField(null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)