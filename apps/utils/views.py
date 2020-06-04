import requests
from lxml import html
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
etree = html.etree


class GetSelfGrade(APIView):
    # formdata字典
    payload = {
        '__VIEWSTATE': '',
        'txtUserName': '',
        'Textbox1': '',
        'TextBox2': '',
        'txtSecretCode': '',
        'RadioButtonList1': '学生',
        'Button1': '',
        'lbLanguage': '',
        'hidPdrs': '',
        'hidsc': ''
    }

    # headers
    headers = {
        'UserAgent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 '
                     'Safari/537.36 '
    }

    # 请求
    url = 'http://jwxt.ahujhc.cn/'

    # dataform
    dataform = {
        '__VIEWSTATE': '',
        'ddlXN': '',
        'ddlXQ': '',
        'txtQSCJ': '0',
        'txtZZCJ': '10',
        'btn_xq': '',
        'ddl_kcxz': ''
    }
    s = requests.Session()

    def get(self, request):
        img = self.s.get(self.url + 'CheckCode.aspx', stream=True, headers=self.headers)
        # 保存验证码图片在当前文件夹下: checkcode.gif
        with open('media/checkcode.gif', 'wb') as f:
            f.write(img.content)
        path = 'http://39.96.72.145/media/checkcode.gif'
        # path = 'http://127.0.0.1:8000/media/checkcode.gif'
        return Response(path)

    def post(self, request):
        sno = str(request.data['sno'])
        self.payload['txtUserName'] = sno
        self.payload['TextBox2'] = str(request.data['spw'])
        # 输入验证码
        self.payload['txtSecretCode'] = str(request.data['check_code'])
        self.dataform['ddlXN'] = str(request.data['xn'])
        self.dataform['ddlXQ'] = str(request.data['xq'])


        # 返回html
        ht = self.s.get(self.url, headers=self.headers)
        # 拿到cookie
        # cookies = ht.cookies

        # 解析
        # 获取VIEWSTATE
        index = etree.HTML(ht.text)
        table = index.xpath('//input[@name="__VIEWSTATE"]/@value')
        self.payload['__VIEWSTATE'] = table
        pst = self.s.post(self.url, data=self.payload, headers=self.headers)

        refer_url = 'http://jwxt.ahujhc.cn/xs_main.aspx?xh={}'.format(sno)
        name_page = self.s.get(url=refer_url, headers=self.headers)
        name_page = etree.HTML(name_page.text)
        try:
            name = name_page.xpath('//div[@class="info"]//em//text()')[1].replace('同学', '')
        except:
            return Response({"msg": "登陆失败，请检查你的信息！"}, status=status.HTTP_400_BAD_REQUEST)
        name = name.encode('gb2312')

        # for c in cookies:
        #     cookie = c.name + '=' + c.value
        # 解决重定向

        # 成绩地址???如何构造出来
        url_grade = 'http://jwxt.ahujhc.cn/Xscjcx.aspx?xh={}&xm={}&gnmkdm=N121613'.format(sno, name)
        headers_change = {
            'UserAgent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/73.0.3683.86 Safari/537.36',
            'Referer': refer_url,
            # 'Cookie': cookie
        }

        # 解析查询成绩所在网址，获得viewtable
        ht1 = self.s.get(url_grade, headers=headers_change, allow_redirects=False)
        page1 = etree.HTML(ht1.text)
        table1 = page1.xpath('//input[@name="__VIEWSTATE"]/@value')
        self.dataform['__VIEWSTATE'] = table1
        # 请求查询成绩所在网址
        score = self.s.post(url_grade, headers=headers_change, data=self.dataform)
        # 解析返回结果获得成绩信息
        grade_page = etree.HTML(score.text)
        # 学年 学期 课程代码 课程名称
        four_head = grade_page.xpath('//table[@class="datelist"]/tr[@class="datelisthead"]/td/a/text()')
        #  课程性质 课程归属 学分 绩点 成绩 辅修标记 补考成绩 重修成绩 开课学院 备注 重修标记
        eleven_head = grade_page.xpath('//table[@class="datelist"]/tr[@class="datelisthead"]/td/text()')
        head = four_head + eleven_head
        courses = grade_page.xpath('//table[@class="datelist"]/tr/td/text()')[11:]

        json_data = []
        if len(courses) % 13 == 0:
            # 有length组数据
            length = int(len(courses) / 13)
            m = 0
            n = 13
            dic = {}
            for i in range(length):
                lis = courses[m:n]
                dic[i] = dict(zip(head[0:13], lis))
                json_data.append(dic[i])
                m = m + 13
                n = n + 13
            return Response(json_data)
        else:
            return Response({"msg": "查询到的信息为空，请稍后再试"}, status=status.HTTP_204_NO_CONTENT)


class AuthStudent(GetSelfGrade):
    def post(self, request):
        sno = str(request.data['sno'])
        self.payload['txtUserName'] = sno
        self.payload['TextBox2'] = str(request.data['spw'])
        # 输入验证码
        self.payload['txtSecretCode'] = str(request.data['check_code'])
        # 返回html
        ht = self.s.get(self.url, headers=self.headers)

        # 解析
        # 获取VIEWSTATE
        index = etree.HTML(ht.text)
        table = index.xpath('//input[@name="__VIEWSTATE"]/@value')
        self.payload['__VIEWSTATE'] = table
        pst = self.s.post(self.url, data=self.payload, headers=self.headers)

        refer_url = 'http://jwxt.ahujhc.cn/xs_main.aspx?xh={}'.format(sno)
        name_page = self.s.get(url=refer_url, headers=self.headers)
        name_page = etree.HTML(name_page.text)
        try:
            name = name_page.xpath('//div[@class="info"]//em//text()')[1].replace('同学', '')
            return Response({"msg": name + "认证成功"}, status=status.HTTP_200_OK)
        except:
            return Response({"msg": "认证失败"}, status=status.HTTP_404_NOT_FOUND)


