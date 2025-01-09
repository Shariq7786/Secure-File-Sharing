from django.db import models
from django.conf import settings


class File(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    shared_with = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='shared_files', blank=True)
    uploaded_file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_name = models.CharField(max_length=255)
    sha256_hash = models.CharField(max_length=64, blank=True)
    nonce = models.BinaryField(null=True, blank=True)

