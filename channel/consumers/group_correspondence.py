from channels.generic.websocket import AsyncWebsocketConsumer
from django import http
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
"""
在消费者类外进行消息推送，推送消息给多个客户端需要利用channel layer
Channel引入了一个layer的概念，channel layer是一种通信系统，允许多个consumer实例之间互相通信，以及与外部Django程序实现互通。

Channel layer主要实现了两种概念抽象：
channel name:
channel实际上是一个发送消息的通道，每个channel都有一个名称，每一个拥有这个名称的人都可以往channel里面发送消息

group:
多个channel可以组成一个group,每个group都有一个名称。
每个拥有这个名称的人都可以往这个group里添加/删除channel，也可以往group里发送消息。
group内的所有channel都可以收到，但是不能给group内的具体某个channel发送消息。

"""

# 异步
class GroupConsumer(AsyncWebsocketConsumer):

    channel_layer_alias = 'default' #调用default的channel_layer
    # 连接时触发
    async def connect(self):
        # query_params = http.QueryDict(self.scope.get("query_string", ""))
        # print(query_params)
        # if query_params.get('token') !="hvag":
        #     await self.close()
        # channel表示一个客户端和服务器websocket连接
        #将channel_name进行分组,后面可以通过组名来分发消息给同一个组的所有channel
        #这里特别说明一下，组名是自定义的，自行对channel进行分组
        kwargs = self.scope["url_route"]["kwargs"] # self.scope 类似于 django request
        #kwargs 获取 url中的uri参数
        self.group_name = kwargs.get('group_name')
        if not self.group_name:
            await self.close()

        print(self.channel_name,'----',self.group_name) # 这里需要保存下来方便外部调用
        await  self.channel_layer.group_add(
            self.group_name, self.channel_name
        )
        await self.accept()

    async def disconnect(self, code):
        # 关闭连接时触发
        #将连接的websock的channel_name 进行持久化，通常与用户名进行绑定
        # 只有定义了通道层(如redis),才能获取到channel_name,否则会报错
        # 当一个客户端关闭websocket的时候 就把这个通道从组中删除
        await self.channel_layer.group_discard(
            self.group_name, self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        # 收到消息后触发 通过发送给组 让组中所有通道接收到消息
        print(text_data)
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'handle_message',
                'message':text_data # 注意这里的message参数 是和 type对一个的函数中 event参数对应
            }
        )

    async def handle_message(self,event): # 这个函数名字 后续需要使用
        print(event) # {'type': 'handle_message', 'message': 'yyyyyyyyyyyyy'}
        message = "hvag:" + event["message"]
        await self.send(text_data=message)

# 配合使用celery
# class TailfConsumer(WebsocketConsumer):
#     def connect(self):
#         self.file_id = self.scope["url_route"]["kwargs"]["id"]
#         self.result = tailf.delay(self.file_id,self.channel_name)
#         # self.result = add.delay(1,8)
#         self.accept()
#     def disconnect(self, code):
#         self.result.revoke(terminate=True)
#     def send_message(self,event):
#         self.send(text_data=json.dumps({"message":event["message"]}))



def send_message(message, channel_name=None, group_name=None, typed=None, alias='default'):
    """
    这个函数是外部调用 由服务器主动推送信息给客户端
    @text str 需要后端主动发送的消息
    @channel_name str 通道名字 是建立通道的时候系统建立的 需要保存下来 然后这里使用
    @group_name str 自己定义的组名
    @typed 消息处理函数
    """

    channel_layer = get_channel_layer(alias)

    #发送到指定的channel,并将消息转发到type中的方法进行处理
    if channel_name:
        async_to_sync(channel_layer.send)(channel_name, {
            "type": typed,
            "message": message,
        })
    # 发送到组里所有的channel
    elif group_name:
        async_to_sync(channel_layer.group_send)(group_name,{
            "type": typed,
            "message": message,
        })

    else:
        raise
 #

# 同步程序 当程序中包含了很多同步io阻塞代码的时候 最好选择同步 以保持整个consumer在单个线程中并避免阻塞整个event
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import datetime
 
 
class ChatConsumer(WebsocketConsumer):
 # websocket建立连接时执行方法
 def connect(self):
     # 从url里获取聊天室名字，为每个房间建立一个频道组
     self.room_name = self.scope['url_route']['kwargs']['room_name']
     self.room_group_name = 'chat_%s' % self.room_name

     # 将当前频道加入频道组
     async_to_sync(self.channel_layer.group_add)(
         self.room_group_name,
         self.channel_name
     )

     # 接受所有websocket请求
     self.accept()

 # websocket断开时执行方法
 def disconnect(self, close_code):
     async_to_sync(self.channel_layer.group_discard)(
         self.room_group_name,
         self.channel_name
     )

 # 从websocket接收到消息时执行函数
 def receive(self, text_data):
     text_data_json = json.loads(text_data)
     message = text_data_json['message']

     # 发送消息到频道组，频道组调用chat_message方法
     async_to_sync(self.channel_layer.group_send)(
         self.room_group_name,
         {
             'type': 'chat_message',
             'message': message
         }
     )

 # 从频道组接收到消息后执行方法
 def chat_message(self, event):
     message = event['message']
     datetime_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

     # 通过websocket发送消息到客户端
     self.send(text_data=json.dumps({
         'message': f'{datetime_str}:{message}'
     }))
