# serializers.py
from rest_framework import serializers
from .models import Image

class ImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields='__all__'
