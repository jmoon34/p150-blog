# Generated by Django 2.2 on 2019-07-09 19:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20190709_1209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testscores',
            name='name',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
