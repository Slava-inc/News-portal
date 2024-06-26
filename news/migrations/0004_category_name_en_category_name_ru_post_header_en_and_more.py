# Generated by Django 5.0.6 on 2024-06-25 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_alter_category_subscribers'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='name_en',
            field=models.CharField(max_length=150, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='category',
            name='name_ru',
            field=models.CharField(max_length=150, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='post',
            name='header_en',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='header_ru',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
