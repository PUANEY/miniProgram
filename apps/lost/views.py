from .models import FiveTaskModel
from rest_framework.views import APIView
from .serializers import FiveTaskSerializers
from rest_framework.response import Response
from rest_framework import status


class FiveTaskViewSet(APIView):
    def get(self, request, category):
        ft = FiveTaskModel.objects.filter(category=category)
        serializer = FiveTaskSerializers(ft, many=True)
        return Response(serializer.data)

    def post(self, request):
        user_id = request.data['user_id']
        category = request.data['category']
        title = request.data['title']
        addr = request.data['addr']
        name = request.data['name']
        telephone = request.data['telephone']
        desc = request.data['desc']
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