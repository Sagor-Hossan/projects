# Generated by Django 5.0.3 on 2024-06-28 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fit_app', '0008_customuser_user_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='about',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='location',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
