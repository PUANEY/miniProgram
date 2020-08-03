from .models import FiveTaskModel
from rest_framework.views import APIView
from .serializers import FiveTaskSerializers
from rest_framework.response import Response
from rest_framework import status
from miniProgram.settings import APP_ID, APP_KEY
from django.contrib.auth import get_user_model

import requests
import json
User = get_user_model()


class FiveTaskViewSet(APIView):   
    def get(self, request, category):
        ft = FiveTaskModel.objects.filter(category=category).order_by('-pub_time')
        serializer = FiveTaskSerializers(ft, many=True)
        return Response(serializer.data)

    def post(self, request):
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'.format(APP_ID, APP_KEY)
        r = requests.get(url).text
        access_token = json.loads(r)['access_token']
        check_url = 'https://api.weixin.qq.com/wxa/servicemarket?access_token={}'.format(access_token)

        user_id = request.data['user_id']
        category = request.data['category']
        title = str(request.data['title'])
        addr = str(request.data['addr'])
        name = str(request.data['name'])
        telephone = str(request.data['telephone'])
        desc = request.data['desc']
        TEXT = str(title + addr + name + desc)
        check_text = {
            "service": "wxee446d7507c68b11",
            "api": "msgSecCheck",
            "client_msg_id": "client_msg_id_1",
            "data": {
                "Action": "TextApproval",
                "Text": TEXT
            }
        }
        check_req = requests.post(check_url, json.dumps(check_text))
        try:
            err_text = json.loads(json.loads(check_req.text)['data'])['Response']['EvilTokens']
        except:
            return Response({"msg": "内容安全检测出现故障，请联系管理员"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if len(err_text):
            return Response({"msg": "您的内容包含敏感词汇，请重新输入!"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            img = request.data['img']
        except:
            img = None
        ft = FiveTaskModel()
        ft.user_id = user_id
        ft.category = category
        ft.title = title
        ft.addr = addr
        ft.name = name
        ft.telephone = telephone
        ft.desc = desc
        if img is not None:
            ft.img = img
        ft.save()
        return Response({"msg": "发布成功"}, status=status.HTTP_201_CREATED)

    def delete(self, request):
        fivetask_id = request.data['fivetask_id']
        if_ft = FiveTaskModel.objects.get(id=fivetask_id)
        if if_ft:
            if_ft.delete()
            return Response({"msg": "删除成功!"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"msg": "该贴已被删除!"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        fivetask_id = request.data['fivetask_id']
        category = request.data['category']
        user_id = request.data['user_id']
        # 一起运动
        if category == 'run':
            if_ft = FiveTaskModel.objects.get(id=fivetask_id)
            if_existed_join_user = if_ft.join_users.filter(id=user_id)
            user = User.objects.get(id=user_id)
            if not if_existed_join_user:
                if_ft.join_users.add(user)
                if_ft.isMe = True
                if_ft.nums += 1
            else:
                if_ft.join_users.remove(user)
                if_ft.nums -= 1
                if_ft.isMe = False
        else:
            # 跑腿
            if_ft = FiveTaskModel.objects.get(id=fivetask_id)
            if_ft.isMe = True
        if_ft.save()
        return Response({"msg": "修改成功"}, status=status.HTTP_200_OK)
