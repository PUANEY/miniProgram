"""
Creator: PUANEY
QQ:1159336305
"""

import xadmin
from django.urls import include, re_path, path
from django.conf.urls import url
from .settings import STATIC_ROOT
from .settings import MEDIA_ROOT
from django.views.static import serve
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static


from users import views
from news.views import NewsListViewSet, NewsCommentViewSet, BannerListViewSet
from confession.views import PostViewSet, PostCommentViewSet, LikeNumViewSet, LikeShowViewSet
from search.views import SearchRecordView, HotRankViewSet, UserSearchRecordViewSet
from lost.views import FiveTaskViewSet
from utils.views import GetSelfGrade, AuthStudent

router = DefaultRouter()
# 新闻列表
router.register(r'newsList', NewsListViewSet)
# 新闻轮播图
router.register(r'banner', BannerListViewSet)
# 帖子列表
router.register(r'post', PostViewSet)
# 帖子点赞展示
router.register(r'likeshow', LikeShowViewSet)
# 关键词热搜榜
router.register(r'hotrank', HotRankViewSet)
# 用户搜索记录
router.register(r'user_record', UserSearchRecordViewSet)


urlpatterns = [
    re_path(r'xadmin/', xadmin.site.urls),
    # 登陆接口
    path('login/', views.WechatLoginView.as_view()),
    # 验证接口
    path('auth/', views.CheckTokenView.as_view()),
    # 点赞接口
    path('like/', LikeNumViewSet.as_view()),
    # 帖子评论get接口
    path('post_comments/<int:post_id>/', PostCommentViewSet.as_view()),
    # 帖子post, delete接口
    path('post_comments/', PostCommentViewSet.as_view()),
    # 新闻评论get接口
    path('news_comments/<int:news_id>/', NewsCommentViewSet.as_view()),
    # 新闻评论post, delete接口
    path('news_comments/', NewsCommentViewSet.as_view()),
    # 物品丢失 拾取 报修 一起运动 跑腿
    path('task/<str:category>/', FiveTaskViewSet.as_view()),
    path('task/', FiveTaskViewSet.as_view()),
    # 关键词搜索接口
    path('search/', SearchRecordView.as_view()),
    # 成绩查询接口
    path('grade/', GetSelfGrade.as_view()),
    # 教务系统认证接口
    path('is_stu/', AuthStudent.as_view()),

    # 图片文件存储地址
    re_path(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    # 文档接口
    re_path(r'docs/', include_docs_urls(title='校园生活')),
    re_path(r'^', include(router.urls)),
    # 富文本
    url(r'^ueditor/', include('DjangoUeditor.urls')),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
