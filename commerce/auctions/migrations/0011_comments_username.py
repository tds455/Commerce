# Generated by Django 4.0.2 on 2022-03-03 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_alter_comments_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='username',
            field=models.CharField(default='Daboss', max_length=64),
            preserve_default=False,
        ),
    ]
