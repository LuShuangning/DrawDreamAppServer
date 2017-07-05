from django.db import models
from app_server.Models.UserInfo import UserInfo
from app_server.Models.NewsDetail import NewsDetail


class UserCollect(models.Model):
    usco_usin_id = models.ForeignKey(UserInfo, primary_key=True)
    usco_nede_id = models.ForeignKey(NewsDetail)
    usco_create_date = models.DateField(auto_now_add=True)

    class Meta:
        db_table = "user_collect"

    def __str__(self):
        return self.usco_usin_id