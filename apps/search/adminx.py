import xadmin
from .models import SearchRecordsModel, UserSearchRecordsModel


xadmin.site.register(SearchRecordsModel)
xadmin.site.register(UserSearchRecordsModel)