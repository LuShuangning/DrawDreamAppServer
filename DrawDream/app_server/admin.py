from django.contrib import admin
from app_server.Models.Account import Account
from app_server.Models.UserInfo import UserInfo
from app_server.Models.NewsClassify import NewsClassify
from app_server.Models.NewsDetail import NewsDetail
from app_server.Models.UserCollect import UserCollect
from app_server.Models.CommentReplay import CommentReplay

# Register your models here.

admin.site.register(NewsClassify)
admin.site.register(NewsDetail)
admin.site.register(CommentReplay)
admin.site.register(UserCollect)
admin.site.register(UserInfo)
admin.site.register(Account)

