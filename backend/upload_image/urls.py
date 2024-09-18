from django.urls import path
from .views import upload_image, get_csrf_token, get_images, deleteImage, updateImage , AddonImage , DeleteSingleImage
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('upload/', upload_image, name='upload_image'),
    path('get_csrf_token/', get_csrf_token, name='get_csrf_token'),
    path('media/images/', get_images, name='get_images'),
    path('delete/<int:id>/', deleteImage, name='delete_image'), 
    path('get-images/<int:id>/', updateImage, name='updateImage'),
    path('addonimage/<int:id>/', AddonImage , name='AddonImage'),
    path('DeleteSingleImage/<int:id>/', DeleteSingleImage , name='DeleteSingleImage')
      # Use angle brackets for capturing parameters
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
