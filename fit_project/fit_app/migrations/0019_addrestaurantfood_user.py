# Generated by Django 5.0.6 on 2024-07-02 10:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fit_app', '0018_alter_addrestaurantfood_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='addrestaurantfood',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
