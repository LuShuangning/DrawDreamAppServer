from django.db import models
from app_server.Models.UserInfo import UserInfo
from app_server.Models.NewsDetail import NewsDetail


class Comment(models.Model):
    core_nede_id = models.ManyToManyField(NewsDetail)
    core_usin_id = models.ManyToManyField(UserInfo)
    core_content = models.CharField(max_length=512)
    core_date = models.DateField(auto_now_add=True)

    class Meta:
        # Django通过这种方式设置多字段主键，但是实际上会新建一个默认的id作主键
        # unique_together = ("core_acco_id", "core_nede_id")
        db_table = "comment"

    def __str__(self):
        return self.core_content
