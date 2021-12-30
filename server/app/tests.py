from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.core.files import File 
from django.core.files.uploadedfile import SimpleUploadedFile 

class AccountTests(APITestCase):
    # 测试开始前
    # def setUp(self) -> None:
    #     #self.client.login(username='hvag', password='secret') 登录
    #     self.client.credentials(HTTP_AUTHORIZATION='Token ' + 'xcvdfafda') # token 认证
    
    # 传递json
    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('app:api',kwargs={'version':'v1'})
        data = {'username': 'abc888','password':'123','confirmpassword':'123'}
        
        # 默认情况下，format可用的格式是 'multipart' 和 'json' 。为了与 Django 现有的 RequestFactory 兼容，默认格式是 'multipart'。
        response = self.client.post(url, data, format='json')
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.get(name='abc888').name, 'abc888')
        
        # 传递file
    def test_upload(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('app:api',kwargs={'version':'v1'})
        file = File(open('media/testfiles/vid.mp4', 'rb'))
        filename = "hvag"
        uploaded_file = SimpleUploadedFile(filename, file.read(), content_type='multipart/form-data') 
        data = {'id': 4,'file':uploaded_file}
        response = self.client.post(url, data, format='multipart')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.get(name='abc888').name, 'abc888')
        
    def test_get(self):
        url = reverse('app:api',kwargs={'version':'v1'})
        response = self.client.get(url, {'name': self.name})
        self.assertEqual(response.status_code, 200)  # 期望的Http相应码为200
        data = response.json()
        self.assertEqual(data['msg'], 'Hello Django I am a test Case')  # 期望的msg返回结果为'Hello Django I am a test Case'



    # 测试结束执行
    # def tearDown(self) -> None:
    #     self.client.logout() #退出登录

"""
shell中运行
1.app模块下的test_create_account 方法
python manage.py test app.tests.AccountTests.test_create_account
2.app模块下的AccountTests类的所有方法
python manage.py test app.tests.AccountTests
3.app模块下的所有测试方法
python manage.py test app
4.运行all
python manage.py test
"""
