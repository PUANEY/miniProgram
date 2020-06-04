from .models import SearchRecordsModel, UserSearchRecordsModel
from .serializers import SearchRecordsSerializer, UserSearchRecordsSerializer
from rest_framework.views import APIView
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework import status
import requests
from lxml import html
import json
import re
from datetime import datetime
import random
etree = html.etree


class SearchRecordView(APIView):
    def post(self, request):
        keywords = request.data['keywords']
        user_id = request.data['user_id']
        platform = request.data['platform']
        data = self.search_platform(platform, keywords)
        length = len(data)
        if keywords == '输入要搜索的课程':
            if length:
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({'msg': "搜索引擎出现错误，请稍后再试"}, status=status.HTTP_204_NO_CONTENT)
        try:
            search_record = SearchRecordsModel.objects.get(keywords=keywords, platform=platform)
            search_record.times += 1
            search_record.save()
            try:
                user_search_record = UserSearchRecordsModel.objects.get(user_id=user_id, record=search_record)
                user_search_record.search_time = datetime.now()
                user_search_record.save()
            except:
                UserSearchRecordsModel.objects.create(user_id=user_id, record=search_record)
        except:
            record = SearchRecordsModel.objects.create(keywords=keywords, platform=platform)
            UserSearchRecordsModel.objects.create(user_id=user_id, record=record)
        if not length:
            return Response({'msg': "搜索引擎出现错误，请稍后再试"}, status=status.HTTP_204_NO_CONTENT)
        return Response(data, status=status.HTTP_200_OK)

    def search_platform(self, platform, keywords):
        if keywords == '输入要搜索的课程' or None:
            if platform == 'bili':
                data = self.get_bili_info('python')
            if platform == 'txkt':
                data = self.get_txkt_info('java')
            if platform == 'uii':
                data = self.get_uii_info('AE')
            return data

        if platform == 'bili':
            data = self.get_bili_info(keywords)
        if platform == 'txkt':
            data = self.get_txkt_info(keywords)
        if platform == 'uii':
            data = self.get_uii_info(keywords)
        return data

    def get_bili_info(self, keywords):
        url = 'https://search.bilibili.com/all?keyword={}&from_source=nav_search_new&order=click&duration=0&tids_1=0'.format(
            keywords)
        headers = self.get_headers()
        r = requests.get(url, headers=headers)
        page = etree.HTML(r.text)
        try:
            script = page.xpath('//script/text()')[2].replace("window.__INITIAL_STATE__=", '').replace(
                ';(function(){var s;(s=document.currentScript||document.scripts[document.scripts.length-1]).parentNode.removeChild(s);}());',
                '')
        except:
            return []
        script = json.loads(script)
        result = script['flow']
        result1 = result['getMixinFlowList-jump-duration-0-keyword-{}-order-click-tids_1-0'.format(keywords)]
        result2 = result1['result']
        # 视频封面
        imgs = []
        for i in range(len(result2)):
            imgs.append(result2[i]['pic'])

        # 视频标题
        titles = page.xpath('//li/a/@title')

        # 视频链接
        hrefs = page.xpath('//li//a[@class="img-anchor"]/@href')

        # 视频简介
        introductions = page.xpath('//li//div[@class="des hide"]//text()')

        # 视频时长
        duations = page.xpath('//li//span[@class="so-imgTag_rb"]//text()')

        # 视频发布时间
        up_dates = page.xpath('//li//span[@title="上传时间"]//text()')

        # 视频浏览量
        visits = page.xpath('//li//span[@title="观看"]//text()')

        data = []
        keys = ['title', 'img', 'href', 'introduction', 'duation', 'up_date', 'visit']

        # 先将列表中的每一项放入字典中
        for i in range(len(titles)):
            values = []
            dic = {}
            values.append(titles[i])
            values.append(imgs[i])
            values.append(hrefs[i])
            values.append(introductions[i].replace('\n', '').strip())
            values.append(duations[i])
            values.append(up_dates[i].replace('\n', '').strip())
            values.append(visits[i].replace('\n', '').strip())
            dic[i] = dict(zip(keys, values))
            data.append(dic[i])
        return data

    def get_txkt_info(self, keywords):
        url = 'https://ke.qq.com/course/list/{}?price_min=0&price_max=0'.format(keywords)
        headers = self.get_headers()
        r = requests.get(url, headers=headers)
        page = etree.HTML(r.text)

        # 视频封面
        imgs = page.xpath('//div[@class="main-left"]//li//img/@src')

        # 视频标题
        titles = page.xpath('//div[@class="main-left"]//h4/a/text()')

        # 视频链接
        hrefs = page.xpath('//div[@class="main-left"]//li//h4/a/@href')

        # 视频节数
        tasks = page.xpath('//li//span[contains(@class, "item-task")]/text()')

        # 最近报名人数
        joins = page.xpath('//li//span[contains(@class, "item-user")]/text()')

        data = []
        keys = ['title', 'img', 'href', 'task', 'join']

        # 先将列表中的每一项放入字典中
        for i in range(len(titles)):
            values = []
            dic = {}
            values.append(titles[i])
            values.append(imgs[i])
            values.append(hrefs[i])
            values.append(tasks[i])
            values.append(joins[i].replace('\n', '').strip())
            dic[i] = dict(zip(keys, values))
            data.append(dic[i])
        return data

    def get_uii_info(self, keywords):
        url = 'https://uiiiuiii.com/?source=post&s={}'.format(keywords)
        headers = self.get_headers()
        r = requests.get(url, headers=headers)
        page = etree.HTML(r.text)
        # 标题
        titles = page.xpath('//div[@class="item"]/h2/a/text()')[1:39:2]

        # 缩略图
        imgs = page.xpath('//div[@class="item"]/div[@class="item-thumb"]//i/@style')
        pattern = re.compile(r'https://images.uiiiuiii.com/wp-content/uploads/\w{4}/\w{2}.*\.\w{3}')

        # 链接
        hrefs = page.xpath('//div[@class="item"]/div[@class="item-thumb"]/a/@href')

        # 描述
        descs = page.xpath('//div[@class="item"]/div[@class="item-entry"]/text()')

        # 发布时间
        pub_times = page.xpath('//div[@class="item"]/div[@class="item-meta"]/span[@class="time"]/text()')

        # 水平
        levels = page.xpath('//div[@class="item"]/div[@class="item-meta"]//span[@class="clevel"]/text()')

        data = []
        keys = ['title', 'img', 'href', 'desc', 'pub_time', 'level']

        # 先将列表中的每一项放入字典中
        for i in range(len(titles)):
            values = []
            dic = {}
            values.append(titles[i].strip())
            values.append(pattern.findall(imgs[i])[0])
            values.append(hrefs[i])
            values.append(descs[i].replace('\r\n', '').strip())
            values.append(pub_times[i].replace('\n', '').strip())
            values.append(levels[i])
            dic[i] = dict(zip(keys, values))
            data.append(dic[i])
        return data

    def get_headers(self):
        user_agent_list = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]
        user_agent = random.choice(user_agent_list)
        headers = {'User-Agent': user_agent}
        return headers


class HotRankViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = SearchRecordsModel.objects.all().order_by('-times')
    serializer_class = SearchRecordsSerializer

    def post(self, request):
        platform = request.data['platform']
        keywords = SearchRecordsModel.objects.filter(platform=platform)[0:10]
        serializer = SearchRecordsSerializer(keywords, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserSearchRecordViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = UserSearchRecordsModel.objects.all().order_by('-search_time')
    serializer_class = UserSearchRecordsSerializer

    def post(self, request):
        user_id = request.data['user_id']
        records = UserSearchRecordsModel.objects.filter(user_id=user_id)
        serializer = UserSearchRecordsSerializer(records, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

