from rest_framework import viewsets, mixins
from .serializers import PostCommentSerializers, PostSerializers, LikeNumSerializers
from .models import PostModel, PostCommentModel, LikeNumModel
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from notification.models import NotifyModel
from miniProgram.settings import APP_KEY, APP_ID
import requests
import json


class PostViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = PostModel.objects.all().order_by('-create_time')
    serializer_class = PostSerializers

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.visit += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def post(self, request):
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'.format(APP_ID, APP_KEY)
        r = requests.get(url).text
        access_token = json.loads(r)['access_token']
        check_url = 'http://api.weixin.qq.com/wxa/servicemarket?access_token={}'.format(access_token)

        user_id = request.data['user_id']
        title = request.data['title']
        desc = request.data['desc']


        TEXT = str(title + desc)
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
        err_text = json.loads(json.loads(check_req.text)['data'])['Response']['EvilTokens']
        if len(err_text):
            return Response({"msg": "您的内容包含敏感词汇，请重新输入!"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            img = request.data['img']
        except:
            img = None
        post = PostModel()
        post.user_id = user_id
        post.title = title
        post.desc = desc
        if img is not None:
            post.img = img
        post.save()
        return Response({"msg": "发帖成功"}, status=status.HTTP_201_CREATED)

    def delete(self, request):
        post_id = request.data['post_id']
        print(self.request)
        if_post = PostModel.objects.get(id=post_id)
        if if_post:
            if_post.delete()
            return Response({"msg": "删除成功!"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"msg": "该贴已被删除!"}, status=status.HTTP_404_NOT_FOUND)


class PostCommentViewSet(APIView):

    def get(self, request, post_id):
        comments = PostCommentModel.objects.filter(post_id=post_id)
        serializer = PostCommentSerializers(comments, many=True)
        return Response(serializer.data)

    def post(self, request):
        # 哪个用户评论的: 获取用户名 username
        # 评论的是哪一篇文章： 获取文章id
        # 评论的内容是什么： 获取评论的content
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'.format(APP_ID, APP_KEY)
        r = requests.get(url).text
        access_token = json.loads(r)['access_token']
        check_url = 'http://api.weixin.qq.com/wxa/servicemarket?access_token={}'.format(access_token)

        user_id = request.data['user_id']
        post_id = request.data['post_id']
        content = request.data['content']

        # 创建消息记录
        nf = NotifyModel()
        nf.notify_type = 2
        nf.target_id = post_id
        nf.sender_id = user_id

        posts = PostModel.objects.get(id=post_id)
        nf.user_id = posts.user_id
        if len(content) <= 7:
            nf.content = '评论了你的' + '\"' + content + '\"'
        else:
            nf.content = '评论了你的' + '\"' + content[:7] + "..." + '\"'
        nf.save()

        check_text = {
            "service": "wxee446d7507c68b11",
            "api": "msgSecCheck",
            "client_msg_id": "client_msg_id_1",
            "data": {
                "Action": "TextApproval",
                "Text": str(content)
            }
        }
        check_req = requests.post(check_url, json.dumps(check_text))
        err_text = json.loads(json.loads(check_req.text)['data'])['Response']['EvilTokens']
        if len(err_text):
            return Response({"msg": "您的内容包含敏感词汇，请重新输入!"}, status=status.HTTP_400_BAD_REQUEST)

        post_comment = PostCommentModel.objects.create(user_id=user_id, post_id=post_id, content=content)
        if post_comment:
            post_comment.save()
            return Response({"msg": "评论成功"}, status=status.HTTP_201_CREATED)
        return Response({"msg": "评论失败,请检查你的网络"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        comment_id = request.data['comment_id']
        if_comment = PostCommentModel.objects.get(id=comment_id)
        if if_comment:
            if_comment.delete()
            return Response({"msg": "删除成功!"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"msg": "该评论已被删除!"}, status=status.HTTP_404_NOT_FOUND)


class LikeNumViewSet(APIView):
    def post(self, request):
        post_id = request.data['post_id']
        user_id = request.data['user_id']
        # 先找到这个帖子
        try:
            posts = PostModel.objects.get(id=post_id)
        except:
            posts = None

        # 创建消息记录
        nf = NotifyModel()
        nf.notify_type = 1
        nf.target_id = post_id
        nf.sender_id = user_id
        nf.user_id = posts.user_id
        content = posts.title
        if len(content) <= 7:
            nf.content = '点赞了你的' + '\"' + content + '\"'
        else:
            nf.content = '点赞了你的' + '\"' + content[:7] + "..." + '\"'
        nf.save()

        like = LikeNumModel.objects.filter(user_id=user_id, post=posts)
        if like.exists():
            like.delete()
            posts.like_num -= 1
            posts.save()
            return Response({'msg': '取消点赞'}, status=status.HTTP_204_NO_CONTENT)
        LikeNumModel.objects.create(user_id=user_id, post=posts, status=True)
        posts.like_num += 1
        posts.save()
        return Response({'msg': "点赞成功"}, status=status.HTTP_200_OK)


class LikeShowViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = LikeNumModel.objects.all().order_by('-like_date')
    serializer_class = LikeNumSerializers










