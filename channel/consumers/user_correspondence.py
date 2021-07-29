from channels.generic.websocket import WebsocketConsumer


# Create your views here.
class UserConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        """
        接收消息
        :param text_data: 客户端发送的消息
        :return:
        """
        print(text_data)

        self.send('hvag' + str(text_data))

"""
只是测试websocket是否连接成功
单个用户通信 用户在前端连接websocket 然后与 后端建立连接 ， 前端发送数据 后端接收数据 并返回
"""