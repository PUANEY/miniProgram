import xadmin
from .models import NewsInfo, NewsComment, Banner, Tag
from xadmin import views


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "江淮小程序后台"
    site_footer = "MiniProgram"


class NewsInfoXadmin(object):
    style_fields = {'content': 'ueditor'}


xadmin.site.register(NewsInfo, NewsInfoXadmin)
xadmin.site.register(Tag)
xadmin.site.register(NewsComment)
xadmin.site.register(Banner)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)