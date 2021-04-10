from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.conf import settings


# Create your models here.
class Staff(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE ,verbose_name="员工所有人")
    username = models.CharField("员工姓名", max_length=50)
    password = models.CharField("员工密码", max_length=128)
    id_card = models.CharField("员工身份证", max_length=50)
    tel = models.CharField("电话号码", max_length=50)
    first_name = models.CharField("店长权限", max_length=50)

    class Meta:
        unique_together = ("owner", "id_card",)
        verbose_name = '员工'
        verbose_name_plural = verbose_name

    def  __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.password = make_password(self.password, settings.SECRET_KEY, 'pbkdf2_sha256')
        super().save(*args, **kwargs)

