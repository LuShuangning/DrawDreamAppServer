from django.db import models


class Account(models.Model):
    acco_id = models.AutoField('文章标识', primary_key=True)
    acco_num = models.CharField('账户', max_length=32, unique=True)
    acco_pwd = models.CharField('密码', max_length=18)
    # 设置auto_now_add或者auto_now为True时会使editable置为False
    acco_create_date = models.DateField(auto_now_add=True)
    acco_modify_date = models.DateField(null=True)
    acco_login_date = models.DateField(null=True)
    acco_count = models.IntegerField(default=0)

    class Meta:
        db_table = "account"

    def __str__(self):
        return self.acco_num
