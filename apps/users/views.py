from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from miniProgram.settings import APP_ID, APP_KEY
import json
import requests
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from rest_framework_jwt.settings import api_settings
from .models import TokenVerify
User = get_user_model()


class WechatLoginView(APIView):
    """
    微信登陆逻辑
    """
    def post(self, request):
        # 前端发送code到后端，后端发送网络请求到微信服务器换取openid
        code = request.data['code']
        username = request.data['nickName']
        gender = request.data['gender']
        avatarUrl = request.data['avatarUrl']

        if not code:
            return Response({'message': '缺少code'}, status=status.HTTP_400_BAD_REQUEST)
        url = "https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code" \
            .format(APP_ID, APP_KEY, code)
        r = requests.get(url)
        res = json.loads(r.text)
        openid = res['openid'] if 'openid' in res else None
        if not openid:
            return Response({'message': '微信调用失败'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        # ------ 现在已经拿到了openid, session_key

        # 保存openid，需要先判断数据库中有没有这个openid
        user = User.objects.filter(openid=openid).first()
        if not user:
            user = User.objects.create(username=username, openid=openid, gender=gender, avatarUrl=avatarUrl)
            user.set_password(openid)
        # 手动签发jwt
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        TokenVerify.objects.create(token=token)

        resp_data = {
            "user_id": user.id,
            "username": user.username,
            "avatarUrl": user.avatarUrl,
            "gender": user.gender,
            "token": token,
        }
        return Response(resp_data)


class CheckTokenView(APIView):
    def post(self, request):
        print(request.data)
        token = request.data['token']
        tokenVer = TokenVerify.objects.get(token=token)
        if tokenVer:
            seven_days_ago = datetime.now() - timedelta(days=7)
            if seven_days_ago > tokenVer.create_date:
                return Response({'msg': 'token已过期'}, status=status.HTTP_400_BAD_REQUEST)
            if tokenVer.token != token:
                return Response({'meg': '错误的token'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'msg': 'token不存在'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'msg': '登陆成功'}, status=status.HTTP_202_ACCEPTED)





