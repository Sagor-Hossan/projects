# Generated by Django 4.2.6 on 2024-06-29 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fit_app', '0012_remove_userfollow_is_following'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
