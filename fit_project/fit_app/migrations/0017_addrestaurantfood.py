# Generated by Django 5.0.6 on 2024-07-01 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fit_app', '0016_postimage_time_userpost_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='addRestaurantFood',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_name', models.CharField(max_length=100)),
                ('calories', models.CharField(max_length=100)),
                ('category', models.CharField(choices=[('fruit', 'Fruit'), ('vegetable', 'Vegetable'), ('grain', 'Grain'), ('protein', 'Protein'), ('dairy', 'Dairy'), ('dessert', 'Dessert'), ('beverage', 'Beverage')], max_length=100)),
                ('description', models.TextField()),
                ('price', models.PositiveIntegerField()),
                ('quantity', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='restaurantFoods')),
            ],
        ),
    ]
