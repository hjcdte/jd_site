# Generated by Django 3.1.5 on 2021-03-24 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0007_auto_20210324_1621'),
    ]

    operations = [
        migrations.AddField(
            model_name='room_date',
            name='is_book',
            field=models.BooleanField(default=1, verbose_name='是否预订'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='room_date',
            name='is_live',
            field=models.BooleanField(default=1, verbose_name='是否入住'),
            preserve_default=False,
        ),
    ]