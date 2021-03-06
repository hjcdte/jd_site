# Generated by Django 3.1.5 on 2021-03-18 21:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Room_Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_type', models.CharField(max_length=50, verbose_name='房间类型')),
                ('price', models.IntegerField(verbose_name='定价')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='房间类型所有人')),
            ],
            options={
                'verbose_name': '房间类型',
                'verbose_name_plural': '房间类型',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_num', models.IntegerField(verbose_name='房间号')),
                ('book_date', models.DateTimeField(blank=True, null=True, verbose_name='入住时间')),
                ('cancel_date', models.DateTimeField(blank=True, null=True, verbose_name='退房时间')),
                ('crash', models.IntegerField(blank=True, null=True, verbose_name='实收房价')),
                ('deposit', models.IntegerField(blank=True, null=True, verbose_name='押金')),
                ('option_live', models.BooleanField(verbose_name='是否已经入住')),
                ('option_book', models.BooleanField(verbose_name='是否已经预订')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='房间所有人')),
                ('room_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.room_type', verbose_name='房间类型')),
            ],
            options={
                'verbose_name': '房间',
                'verbose_name_plural': '房间',
                'unique_together': {('owner', 'room_num')},
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='客户姓名')),
                ('id_card', models.CharField(max_length=50, verbose_name='客户身份证')),
                ('tel', models.CharField(blank=True, max_length=50, verbose_name='电话号码')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='客户所有人')),
            ],
            options={
                'verbose_name': '客户',
                'verbose_name_plural': '客户',
            },
        ),
        migrations.CreateModel(
            name='Booking_record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_date', models.DateTimeField(verbose_name='入住时间')),
                ('cancel_date', models.DateTimeField(verbose_name='退房时间')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.customer', verbose_name='客户')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='记录所有人')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.room', verbose_name='房间号')),
            ],
            options={
                'verbose_name': '住房记录',
                'verbose_name_plural': '住房记录',
            },
        ),
    ]
