# models.py
from django.db import models

class Image(models.Model):
    file = models.ImageField(upload_to='images/')
    print(file)
    caption = models.CharField(max_length=255, blank=True, null=True)  # Optional caption field

class ImageDetail(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    path = models.CharField(max_length=255)
