# Generated by Django 3.1.4 on 2020-12-25 13:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20201223_2240'),
    ]

    operations = [
        migrations.AddField(
            model_name='voting',
            name='author_name',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
