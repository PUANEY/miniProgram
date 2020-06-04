import xadmin
from .models import PostModel, PostCommentModel, LikeNumModel


xadmin.site.register(PostModel)
xadmin.site.register(PostCommentModel)
xadmin.site.register(LikeNumModel)
