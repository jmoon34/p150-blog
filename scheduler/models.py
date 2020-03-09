from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import date
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class Event(models.Model):
    title = models.CharField(max_length=150, blank=True, null=True)
    description = RichTextUploadingField(config_name='default', blank=True,
                                         null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def check_overlap(self, start_1, end_1, start_2, end_2):
        if start_2 == end_1 or end_2 == start_1:
            return False
        elif(start_2 >= start_1 and start_2 <= end_1) or (end_2 >= start_1 and
                                                          end_2 <= end_1):
            return True
        elif start_2 <= start_1 and end_2 >= end_1:
            return True

    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError('End time must be after starting time')

        events = Event.objects.filter(start_time__date=date(self.start_time.year,
                                                           self.start_time.month,
                                                          self.start_time.day)).exclude(pk=self.pk)
        if events.exists():
            for event in events:
                if self.check_overlap(event.start_time, event.end_time,
                                      self.start_time, self.end_time):
                    raise ValidationError('There is an overlap with another \
                                          event: ' + str(event.title))

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('event-detail', kwargs={'pk': self.pk})
