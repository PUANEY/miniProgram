from django.db import models
from django.contrib.auth import get_user_model
from uuid import uuid4

User = get_user_model()
image_file = uuid4().hex


class FiveTaskModel(models.Model):
    """
    丢失 拾取物品 报修 跑腿 一起运动模型
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="发布人")
    category = models.CharField(max_length=60, verbose_name="类别", choices=(
        ("lost", "失物招领"),
        ("pick", "拾取"),
        ("repair", "报修"),
        ("run", "一起运动"),
        ("paotui", "跑腿")), default="lost")
    title = models.CharField(verbose_name="标题", max_length=255)
    addr = models.CharField(verbose_name="地址", max_length=255)
    name = models.CharField(verbose_name="姓名_时间_薪资", max_length=60, null=True)
    telephone = models.CharField(verbose_name="手机号码", max_length=60, null=True)
    img = models.ImageField(upload_to='lp/images/%y/%d/{image_file}'.format(image_file=image_file),
                             null=True,
                             blank=True,
                             verbose_name='物品图片')
    desc = models.TextField(verbose_name='物品描述', null=True)
    isMe = models.BooleanField(verbose_name="我的任务", default=False)
    pub_time = models.DateTimeField(verbose_name="发布时间", auto_now_add=True)
    nums = models.IntegerField(verbose_name="报名人数", default=0)

    class Meta:
        db_table = 'fivetask'
        verbose_name = '丢失拾取报修跑腿运动'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.category + self.title

