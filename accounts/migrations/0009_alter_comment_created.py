# Generated by Django 4.2.7 on 2023-12-29 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_merge_20231219_1018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created',
            field=models.DateField(auto_now_add=True),
        ),
    ]