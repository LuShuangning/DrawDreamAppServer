from django.db import models
import uuid
# Create your models here.


class Account(models.Model):
    acco_id = models.AutoField(primary_key=True)
    acco_num = models.CharField(max_length=32, unique=True)
    acco_pwd = models.CharField(max_length=18)
    # 设置auto_now_add或者auto_now为True时会使editable置为False
    acco_create_date = models.DateField(auto_now_add=True)
    acco_modify_date = models.DateField(null=True)
    acco_login_date = models.DateField(null=True)
    acco_count = models.IntegerField(default=0)

    class Meta:
        db_table = "account"

    def __str__(self):
        return self.acco_num


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


class NewsClassify(models.Model):
    necl_id = models.UUIDField(primary_key=True,  default=uuid.uuid4, editable=False)
    necl_name = models.CharField(max_length=64, unique=True)
    necl_create_date = models.DateField(auto_now_add=True)

    class Meta:
        db_table = "news_classify"

    def __str__(self):
        return self.necl_name


class NewsDetail(models.Model):
    nede_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nede_classify = models.ForeignKey(NewsClassify, to_field='necl_name')
    # 创建该条数据时的系统时间
    nede_create_date = models.DateField(auto_now_add=True)
    nede_title = models.CharField(max_length=128)
    nede_author = models.CharField(max_length=64, default="佚名")
    # 爬取的文章上的时间，不是爬取文章存进数据库的时间，所以用CharField
    nede_time = models.CharField(max_length=32, null=True)
    nede_content = models.TextField()
    # 阅读次数
    nesu_count = models.IntegerField(default=0)
    # 被喜欢的次数
    nesu_like = models.IntegerField(default=0)

    class Meta:
        db_table = "news_detail"

    def __str__(self):
        return self.nede_title


class UserCollect(models.Model):
    usco_acco_id = models.ForeignKey(Account, primary_key=True)
    usco_acco_id = models.ForeignKey(NewsDetail)
    usco_create_date = models.DateField(auto_now_add=True)

    class Meta:
        db_table = "user_collect"

    def __str__(self):
        return self.usco_acco_id


class CommentReplay(models.Model):
    core_acco_id = models.ForeignKey(Account)
    core_nede_id = models.ForeignKey(NewsDetail)
    core_content = models.CharField(max_length=512)
    core_date = models.DateField(auto_now_add=True)

    class Meta:
        # Django通过这种方式设置多字段主键，但是实际上会新建一个默认的id作主键
        unique_together = ("core_acco_id", "core_nede_id")
        db_table = "comment_reply"

    def __str__(self):
        return self.core_content
