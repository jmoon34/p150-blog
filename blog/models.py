from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from scheduler.models import Event
from django.urls import reverse
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.exceptions import ValidationError
from django.contrib.postgres.search import SearchVectorField

class Category(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog-category')

    def clean(self):
        duplicate = Category.objects.filter(title__iexact=self.title)
        if duplicate.exists():
            raise ValidationError('A category with that name already exists')

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = RichTextUploadingField(config_name='default')
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True,
                                blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True,
                             blank=True, related_name='comments')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True,
                             blank=True, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.post.pk})
