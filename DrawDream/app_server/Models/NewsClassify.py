from django.db import models
import uuid


class NewsClassify(models.Model):
    necl_id = models.UUIDField(primary_key=True,  default=uuid.uuid4, editable=False)
    necl_name = models.CharField(max_length=64, unique=True)
    necl_create_date = models.DateField(auto_now_add=True)

    class Meta:
        db_table = "news_classify"

    def __str__(self):
        return self.necl_name