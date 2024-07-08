from rest_framework import serializers
from .models import *

class jobModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = jobModel
        fields = ('__all__')

class customUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = customUser
        fields = ('__all__')