# Generated by Django 4.0.2 on 2022-03-03 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_listing_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='winnerid',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]