from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from datetime import time

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class TestScores(models.Model):
    two_k = models.TimeField(null=True, blank=True, default=time())
    six_k = models.TimeField(null=True, blank=True, default=time())
    max_watts = models.FloatField(null=True, blank=True, default=0.0)
    name = models.OneToOneField(User, on_delete=models.CASCADE)