from django.db import models
from django.conf import settings


# Create your models here.
class Room_Type(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE ,verbose_name="房间类型所有人")
    room_type = models.CharField("房间类型", max_length=50)
    price = models.IntegerField("定价")

    class Meta:
        verbose_name = '房间类型'
        verbose_name_plural = verbose_name

    def  __str__(self):
        return self.room_type


class Room(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE ,verbose_name="房间所有人")
    room_type = models.ForeignKey(Room_Type, on_delete=models.CASCADE ,verbose_name="房间类型")
    room_num = models.IntegerField("房间号")

    class Meta:
        unique_together = ("owner", "room_num",)
        verbose_name = '房间'
        verbose_name_plural = verbose_name
    
    def  __str__(self):
        room_num = str(self.room_num)
        return room_num


class Room_Date(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE ,verbose_name="记录所有人")
    room = models.ForeignKey(Room, on_delete=models.CASCADE ,verbose_name="房间号")
    book_date = models.DateField("入住时间",  blank=True, null=True)#已入住才记录
    cancel_date = models.DateField("退房时间",  blank=True, null=True)
    is_live = models.BooleanField("是否入住")
    is_book = models.BooleanField("是否预订")
    name = models.CharField("预订客户姓名", max_length=50,  blank=True, null=True)
    tel = models.CharField("预订电话号码", max_length=50,  blank=True, null=True)
    book_day = models.IntegerField("预订天数",blank=True, null=True)
    crash = models.IntegerField("实收房价", blank=True, null=True)
    deposit = models.IntegerField("押金", blank=True, null=True)

    # 入住时间不等于今天且
    # 退房时间小于等于今天

    class Meta:
        verbose_name = '房间时间'
        verbose_name_plural = verbose_name

    def  __str__(self):
        room_num = str(self.room.room_num)
        return room_num


class Customer(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE ,verbose_name="客户所有人")
    name = models.CharField("客户姓名", max_length=50)
    id_card = models.CharField("客户身份证", max_length=50)
    tel = models.CharField("电话号码", max_length=50,  blank=True, null=True)
    
    class Meta:
        verbose_name = '客户'
        verbose_name_plural = verbose_name
    
    def  __str__(self):
        return self.name


class Booking_record(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE ,verbose_name="记录所有人")
    room = models.ForeignKey(Room, on_delete=models.CASCADE ,verbose_name="房间号")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE ,verbose_name="客户")
    book_date = models.DateField("入住时间")#已入住才记录
    cancel_date = models.DateField("退房时间")
    room_registrant = models.CharField("房间操作人", max_length=50)


    class Meta:
        verbose_name = '住房记录'
        verbose_name_plural = verbose_name

    def  __str__(self):
        return self.owner.username


class Money(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE ,verbose_name="记录所有人")
    room = models.ForeignKey(Room, on_delete=models.CASCADE ,verbose_name="房间号")
    crash = models.IntegerField("实收房价")
    book_date = models.DateField("入住时间")#已入住才记录
    cancel_date = models.DateField("退房时间")

    class Meta:
        verbose_name = '营收'
        verbose_name_plural = verbose_name

    def  __str__(self):
        return self.owner.username