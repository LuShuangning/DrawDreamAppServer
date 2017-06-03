from django.db import models
from app_server.Models.Account import Account


class UserInfo(models.Model):
    # ForeignKey默认地使用关联对象的主键。
    usin_id = models.ForeignKey(Account, primary_key=True)
    usin_name = models.CharField(max_length=32, default="漫画小迷弟")
    usin_sex = models.BooleanField()
    usin_phone = models.CharField(max_length=20, unique=True, null=True)
    usin_email = models.EmailField()
    usin_sign = models.CharField(max_length=256, default="这个人很懒，什么也没留下")

    class Meta:
        db_table = "user_info"

    def __str__(self):
        return self.usin_name
