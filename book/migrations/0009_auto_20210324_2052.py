# Generated by Django 3.1.5 on 2021-03-24 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0008_auto_20210324_1955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room_date',
            name='book_date',
            field=models.DateField(blank=True, null=True, verbose_name='入住时间'),
        ),
        migrations.AlterField(
            model_name='room_date',
            name='cancel_date',
            field=models.DateField(blank=True, null=True, verbose_name='退房时间'),
        ),
    ]
