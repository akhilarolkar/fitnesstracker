# Generated by Django 3.1.7 on 2021-11-12 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diet', '0003_profile_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='meal',
            name='carbs',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='meal',
            name='fats',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='meal',
            name='protein',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
    ]
