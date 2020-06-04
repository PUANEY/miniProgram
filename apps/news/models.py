from django.db import models
from datetime import datetime
from DjangoUeditor.models import UEditorField
from django.contrib.auth import get_user_model
User = get_user_model()


class Tag(models.Model):
    name = models.CharField(verbose_name="标签", max_length=255)

    class Meta:
        db_table = 'news_tag'
        verbose_name = '新闻标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class NewsInfo(models.Model):
    title = models.CharField(max_length=100, verbose_name="新闻标题")
    author = models.ForeignKey(User, verbose_name="作者", on_delete=models.CASCADE)
    desc = models.TextField(verbose_name="简介")
    content = UEditorField(verbose_name="正文",
                           imagePath="news/images/",
                           filePath="news/files/",
                           default='',
                           width=700,
                           height=500,
                           toolbars='full',
                           )
    image = models.ImageField(verbose_name="展示图片", upload_to="newsImages")
    visit = models.IntegerField(default=0, verbose_name="浏览量")
    tag = models.ForeignKey(Tag, verbose_name="新闻标签", on_delete=models.CASCADE, default='')
    pub_time = models.DateTimeField(auto_now_add=True, verbose_name="发布时间")

    class Meta:
        db_table = 'news_info'
        verbose_name = '新闻信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class NewsComment(models.Model):
    news = models.ForeignKey(NewsInfo, verbose_name="评论", related_name='news_comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="评论人")
    content = models.TextField(verbose_name="新闻评论内容", max_length=300)
    pub_time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')

    class Meta:
        db_table = 'news_comments'
        verbose_name = '新闻评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.user.username) + ': ' + str(self.content)


class Banner(models.Model):
    """
    轮播的商品
    """
    news = models.ForeignKey(NewsInfo, verbose_name="新闻", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='banner', verbose_name="轮播图片")
    index = models.IntegerField(default=0, verbose_name="轮播顺序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '轮播新闻'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.news.title


