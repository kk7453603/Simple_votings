# Generated by Django 3.1.5 on 2021-01-25 12:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_voteimages'),
    ]

    operations = [
        migrations.AddField(
            model_name='votefact',
            name='voting',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='main.voting'),
            preserve_default=False,
        ),
    ]