from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    avatarUrl = models.URLField(verbose_name="用户头像", default="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI81hOdg7FFbxuBRZGAKHLemY6UjF4QFdTtibgc2C165fPFqNnSC2Hbmb3Ow8wkEoEhaOplK2UeKEw/132")
    openid = models.CharField(max_length=50, unique=True, verbose_name="唯一标识")
    gender = models.CharField(max_length=6, choices=(("male", "男"), ("female", "女")), default="female", verbose_name="性别")


class TokenVerify(models.Model):
    token = models.CharField(max_length=255, verbose_name="令牌")
    create_date = models.DateTimeField(auto_now_add=True)


# 1. 用户点击登陆
# 2. 提示授权，授权后可得到该微信用户的 avatar, username, gender
# 3. 然后调用登陆接口，如果是第一次登陆则会将用户的avatar, username， gender传到后端数据库中保存。
# 4. 以后用户信息中就有用户的id, username, avatar, gender
