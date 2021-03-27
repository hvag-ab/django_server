-- GRANT ALL PRIVILEGES ON sche.* TO my@"%" IDENTIFIED BY "mypass";
GRANT ALL PRIVILEGES ON *.* TO root@"%" IDENTIFIED BY "hvag";
FLUSH PRIVILEGES;

-- GRANT ALL PRIVILEGES ON *.* TO root@"%" IDENTIFIED BY "hvag";
-- FLUSH PRIVILEGES;
-- use mysql;
-- ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY 'hvag';
-- create database test;
use sche;
CREATE TABLE `user` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `username` varchar(150) NOT NULL,
  `password` varchar(128) NOT NULL,
  `email` varchar(128) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `superuser` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `UQE_user_username` (`username`),
  UNIQUE KEY `UQE_user_email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
insert into user (username,`password`,email,superuser) values("hvag","$2a$10$izzPdSAOphONGXV26bClZ.23RSWVpeIBccDwYqT6ZTmc//02jla0C","475886877@qq.com",1);

