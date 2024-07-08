# Generated by Django 5.0.6 on 2024-06-05 04:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0002_rename_company_title_jobmodel_job_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='jobapplymodel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skills', models.CharField(max_length=100, null=True)),
                ('education', models.CharField(max_length=100, null=True)),
                ('resume', models.FileField(null=True, upload_to='static/resume')),
                ('applied_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('apply_to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myApp.jobmodel')),
            ],
        ),
    ]
