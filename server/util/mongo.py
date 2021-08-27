from django.conf import settings
from pymongo import MongoClient, cursor
from bson.objectid import ObjectId
from typing import Optional, Dict, List, Any, Union, Tuple

mongo_uri = settings.MONGO


class MongoConnection:

    def __init__(self, dbname, collection, maxPoolSize=20, minPoolSize=5, maxIdleTimeMS=1000, connectTimeoutMS=1000):
        client = MongoClient(mongo_uri, maxPoolSize=maxPoolSize, minPoolSize=minPoolSize,
                             maxIdleTimeMS=maxIdleTimeMS, connectTimeoutMS=connectTimeoutMS, connect=False)
        self.db = client[dbname]  # 没有就创建
        self.collection = self.db[collection]  # 没有就创建

    def filter(self, id: Optional[str] = None, data: Optional[dict] = None,
               condition: Optional[Dict[str, Dict[str, Any]]] = None,
               many: bool = True
               ) -> Union[dict, None, cursor.Cursor]:
        """
        :param id: 查询mongo的 _id ObjectId对的id获取办法是 ObjectId.binary.hex()
        :param data:查询的条件 精确查询
        :param condition:查询的条件 条件查询例如{'age': {'$gt': 20}} $gt gte lt lte {'$in': [20, 23]} nin {'$exists': True} {'$search': 'Mike'}
        :param many:查询一条还是多条
        :return:find_one 返回 dict or None， find 返回结果是Cursor类型，相当于一个生成器，需要遍历取到所有的结果，每一个结果都是字典类型
        """
        if id:
            return self.collection.find_one({'_id': ObjectId(id)})

        find = getattr(self.collection, 'find' if many else 'find_one')
        if data:
            return find(data)
        if condition:
            return find(condition)
        else:
            return find()

    def create(self, data: Union[dict, list]) -> Union[ObjectId, List[ObjectId]]:
        if isinstance(data, dict):
            result = self.collection.insert_one(data)
            return result.inserted_id
        elif isinstance(data, list):
            result = self.collection.insert_many(data)
            return result.inserted_ids
        else:
            raise TypeError(f'data must be list or dict got ={type(data)}')

    def update(self, condition: Union[dict,Dict[str, Dict[str, Any]]],
               data: dict) -> int:
        """
        :param data: 更新值（替换key-value） 如果key不在查询值里面 就把这个key value新增上去
        :param condition: 查询条件
        :return:
        """
        result = self.collection.update_many(condition, {'$set': data})
        return result.modified_count

    def update_or_create(self, condition:Union[dict,Dict[str, Dict[str, Any]]],
                         data: dict = None) -> int:
        result = self.collection.update_one(condition, {'$set': data}, upsert=True)
        return result.modified_count

    def delete(self, condition:Union[dict,Dict[str, Dict[str, Any]]]) -> int:
        result = self.collection.delete_many(condition)
        return result.deleted_count

    def find_or_create(self, condition:Union[dict,Dict[str, Dict[str, Any]]],
                       data:dict) -> Tuple[bool, dict]:
        result = self.collection.find(condition)
        if not result:
            self.create(data)
            return False, result
        else:
            return True, result

