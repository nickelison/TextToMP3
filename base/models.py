import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.templatetags.static import static
from .utils import delete_from_s3, get_presigned_s3_file_url, get_presigned_cloudfront_file_url

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    profile_picture = models.CharField(max_length=64, default="default.jpg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_profile_picture_url(self):
        if self.profile_picture == 'default.jpg':
            return static('img/avatars/default.jpg')
        
        if settings.PROD:
            #return get_presigned_s3_file_url("avatars/" + self.profile_picture, settings.MEDIA_S3_BUCKET)
            return get_presigned_cloudfront_file_url("avatars/" + self.profile_picture)
        else:
            return os.path.join(settings.MEDIA_URL, 'avatars', self.profile_picture)

class Mp3File(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    custom_file_name = models.CharField(max_length=255)
    file_name = models.CharField(max_length=255)
    text = models.CharField(max_length=3000, default='')
    s3_key = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    def get_mp3_url(self):
        return get_presigned_s3_file_url('mp3/' + self.file_name, settings.MEDIA_S3_BUCKET)
    
    def delete_from_s3(self):
        delete_from_s3(self.s3_key, settings.MEDIA_S3_BUCKET)
        
    def __str__(self):
        return self.custom_file_name
