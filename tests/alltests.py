#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
  This module implements utility that fills database for tests and demos.
"""

import MySQLdb
from models.dborm import Dborm
from config import DATABASE_IP as ip
from config import DATABASE_USER as user
from config import DATABASE_USER_PASS as password
from config import DATABASE_NAME as db_name


def init_database():
    db = MySQLdb.connect(ip, user, password)
    cursor = db.cursor()

    cursor.execute('DROP DATABASE IF EXISTS {0}'.format(db_name))
    db.commit()
    cursor.execute('CREATE DATABASE {0}'.format(db_name))
    db.commit()
    db.close()

    db = MySQLdb.connect(ip, user, password, db_name)

    cursor = db.cursor()
    cursor.execute("""CREATE TABLE users(
                         id INT NOT NULL AUTO_INCREMENT,
                         user varchar(150),
                         PRIMARY KEY (id))""")

    db.commit()

    cursor.execute("""CREATE TABLE videos(
                        id INT NOT NULL AUTO_INCREMENT,
                        user_id INT NOT NULL,
                        url varchar(20),
                        PRIMARY KEY(id),
                        FOREIGN KEY(user_id)
                            REFERENCES users(id)
                            ON DELETE CASCADE)""")

    db.commit()

    db.close()


def test_insert():
    orm = Dborm()

    users = {"user": "test"}
    r = orm.insert('users', users)
    if r is -1:
        raise Exception('Cannot insert data into users')

    urls = {"user_id": "1", "url": "eyewyrtr"}
    r = orm.insert('videos', urls)
    if r is -1:
        raise Exception('Cannot insert data into videos')


def test_select():
    orm = Dborm()
    l = orm.select('users', ['user'])
    if (len(l) == 0):
        raise Exception('Cannot select from table users')

    l = orm.select('videos', ['user_id', 'url'])
    if (len(l) == 0):
        raise Exception('Cannot select from table videos')


def test_update():
    orm = Dborm()
    r = orm.update('users', {'user': 'test1'}, ' WHERE id=1')
    if r is False:
        raise Exception('Cannot update data in table users')


def test_delete():
    orm = Dborm()
    r = orm.delete('users', {'id': '1'})
    if r is False:
        raise Exception('Cannot delete data from table users')


if __name__ == "__main__":
    init_database()
    test_insert()
    test_select()
    test_update()
    test_delete()
