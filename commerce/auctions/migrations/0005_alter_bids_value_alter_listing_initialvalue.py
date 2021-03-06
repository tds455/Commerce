# Generated by Django 4.0.2 on 2022-03-02 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_remove_listing_enddate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bids',
            name='value',
            field=models.DecimalField(decimal_places=2, max_digits=4000000),
        ),
        migrations.AlterField(
            model_name='listing',
            name='initialvalue',
            field=models.DecimalField(decimal_places=2, max_digits=4000000),
        ),
    ]
