# Generated by Django 4.0.2 on 2022-03-03 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_listing_winnerid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='comment',
            field=models.CharField(max_length=600),
        ),
    ]
