from rest_framework.views import APIView
from .serializers import NotifySerializers
from .models import NotifyModel
from rest_framework.response import Response
from confession.models import PostModel, PostCommentModel
from users.models import User


class NotifyView(APIView):

    def post(self, request):
        user_id = request.data["user_id"]
        notify_type = request.data["notify_type"]
        msgList = []
        data = {}
        # 根据消息类型返回记录
        for i in range(4):
            if notify_type == i:
                notify = NotifyModel.objects.filter(user_id=user_id, notify_type=i)
                if i == 0 or i == 3:
                    user = User.objects.get(id=1)
                    for j in notify:
                        s = NotifySerializers(j).data
                        data["avatar_url"] = user.avatarUrl
                        data["nickname"] = user.username
                        data["content"] = s.get("content")
                        data["created_at"] = s.get("created_at")
                        msgList.append(data)
                    break
                for nf in notify:
                    if i == 1 or i == 2:
                        is_existed = PostModel.objects.get(id=nf.target_id)
                    if not is_existed:
                        nf.delete()
                    user = User.objects.get(id=nf.sender_id)
                    s = NotifySerializers(nf).data
                    data["avatar_url"] = user.avatarUrl
                    data["nickname"] = user.username
                    data["content"] = s.get("content")
                    data["created_at"] = s.get("created_at")
                    data["target_id"] = nf.target_id
                    msgList.append(data)
                break
        return Response(msgList)


