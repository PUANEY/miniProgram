from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class SearchRecordsModel(models.Model):
    """
    搜索记录模型
    """
    keywords = models.CharField(max_length=60, verbose_name="搜索关键词")
    platform = models.CharField(max_length=60, verbose_name="平台")
    times = models.IntegerField(verbose_name="搜索次数", default=0)

    class Meta:
        db_table = 'search_records'
        verbose_name = '搜索记录'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.platform) + '---' + str(self.keywords)


class UserSearchRecordsModel(models.Model):
    """
    用户搜索
    """
    user = models.ForeignKey(User, verbose_name="用户", related_name="user_record", on_delete=models.CASCADE)
    record = models.ForeignKey(SearchRecordsModel, verbose_name="搜索记录", related_name="record", on_delete=models.CASCADE)
    search_time = models.DateTimeField(verbose_name="搜索时间", auto_now_add=True)

    class Meta:
        db_table = 'user_search_records'
        verbose_name = "用户搜索记录"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.user.username) + '---' + str(self.record.keywords)