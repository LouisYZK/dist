drop database if exists spider;

create database spider;

use spider;

create table post (
    `title` varchar(200) not null,
    `create_date` date not null,
    `url_object_id` varchar(50) not null,
    `url` varchar(300) not null,
    `praise_numbers` int(11),
    `favor_numbers` int(11),
    `comment_numbers` int(11),
    `tags` varchar(200)
) engine=innodb default charset=utf8;