from django.db import models


class UserInfo(models.Model):
    # ForeignKey默认地使用关联对象的主键。
    usin_id = models.AutoField(primary_key=True)
    # 账号
    usin_num = models.CharField('账号', max_length=32, unique=True)
    # 密码
    usin_pwd = models.CharField('密码', max_length=18)
    # 昵称
    usin_name = models.CharField('昵称', max_length=32, default="漫画小迷弟")
    # 性别
    usin_sex = models.BooleanField()
    # 创建日期 设置auto_now_add或者auto_now为True时会使editable置为False
    usin_create_date = models.DateField('创建日期', auto_now_add=True)
    # 上次登录日期
    usin_login_date = models.DateField('上次登录日期', null=True)
    usin_phone = models.CharField('手机号', max_length=20, unique=True, null=True)
    usin_email = models.EmailField('邮箱')
    usin_sign = models.CharField('签名', max_length=256, default="这个人很懒，什么也没留下")
    usin_count = models.IntegerField('登录次数', default=0)

    class Meta:
        db_table = "user_info"

    def __str__(self):
        return self.usin_name
