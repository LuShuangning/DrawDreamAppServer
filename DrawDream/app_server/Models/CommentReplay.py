from django.db import models
from app_server.Models.Account import Account
from app_server.Models.NewsDetail import NewsDetail


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
