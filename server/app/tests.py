from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

class AccountTests(APITestCase):
    # 测试开始前
    # def setUp(self) -> None:
    #     #self.client.login(username='hvag', password='secret') 登录
    #     self.client.credentials(HTTP_AUTHORIZATION='Token ' + 'xcvdfafda') # token 认证

    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('app:api',kwargs={'version':'v1'})
        data = {'username': 'abc888','password':'123','confirmpassword':'123'}
        response = self.client.post(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.get(name='abc888').name, 'abc888')


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
