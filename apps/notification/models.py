from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class NotifyModel(models.Model):
    content = models.TextField(verbose_name="消息内容", help_text="消息内容")
    notify_type = models.IntegerField(verbose_name="消息类型",
                                      help_text="消息类型",
                                      choices=((0, "活动消息"), (1, "点赞"), (2, "评论"), (3, "官方消息")), default=0)
    target_id = models.IntegerField(verbose_name="目标id", help_text="通过这个目标id和消息类型去找对应的记录", default=1, null=True)
    sender_id = models.IntegerField(verbose_name="发送方用户id", help_text="用户点赞评论等自动发送当前用户id", default=1)
    user_id = models.IntegerField(verbose_name="当前登录的用户id", help_text="根据前端post的user_id来获取对应的消息列表", default=1)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="消息创建时间")

    class Meta:
        db_table = "notify"
        ordering = ["-created_at"]

    def __str__(self):
        return self.content
