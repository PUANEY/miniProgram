from django.db import models
from django.contrib.auth import get_user_model
from uuid import uuid4

User = get_user_model()
image_file = uuid4().hex


class PostModel(models.Model):
    """
    表白墙帖子
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="发布人", related_name='pub_user')
    title = models.CharField(verbose_name="标题", max_length=255)
    desc = models.TextField(verbose_name="帖子内容")

    img = models.ImageField(upload_to='post/images/%y/%d/{image_file}'.format(image_file=image_file),
                             null=True,
                             blank=True,
                             verbose_name='帖子图片')
    create_time = models.DateTimeField(verbose_name="发布时间", auto_now_add=True)
    like_num = models.IntegerField(verbose_name="点赞数", default=0)
    visit = models.IntegerField(default=0, verbose_name="浏览量")

    class Meta:
        db_table = 'post'
        verbose_name = "帖子"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class LikeNumModel(models.Model):
    """
    帖子点赞
    """
    user = models.ForeignKey(User, verbose_name="点赞人", on_delete=models.CASCADE, related_name='user', null=True)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, verbose_name="帖子", null=True)
    status = models.BooleanField(verbose_name="点赞状态", default=False)
    like_date = models.DateTimeField(verbose_name="点赞时间", auto_now_add=True)

    class Meta:
        db_table = 'LikeNum'
        verbose_name = '点赞'
        verbose_name_plural = verbose_name


class PostCommentModel(models.Model):
    """
    表白墙评论
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="评论人")
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, verbose_name="评论的文章", related_name='post')
    # parent_comment = models.ForeignKey('PostCommentModel', blank=True, null=True, related_name='p_comment',
    #                                    verbose_name='父评论', on_delete=models.CASCADE)
    content = models.TextField(verbose_name="评论内容", max_length=300)
    pub_time = models.DateTimeField(verbose_name="评论时间", auto_now_add=True)

    class Meta:
        db_table = 'post_comments'
        verbose_name = "帖子评论记录"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.user.username) + ': ' + str(self.content)

