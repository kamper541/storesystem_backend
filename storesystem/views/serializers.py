from rest_framework import serializers
from storesystem.models import *

class UserSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()