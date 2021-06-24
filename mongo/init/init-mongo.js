db = db.getSiblingDB('test'); // 创建一个名为"test"的DB

// 创建一个名为"test"的用户，设置密码和权限

db.createUser(
    {
        user: "test",
        pwd: "123456",
        roles: [
            { role: "dbOwner", db: "test"}
        ]
    }
);

db.createCollection("log");  // 在"test"中创建一个名为"log"的Collection

// docker exec -it mongo的id bash
//  mongo 127.0.0.1:27017 -u 'root' -p '123456' --authenticationDatabase 'admin'
// use test
// db.log.save({name: 'test', age: '22'})  db.log.find()
