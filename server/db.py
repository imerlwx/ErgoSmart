import sqlite3
import json
from util.index import fetch_dict_result
database_path = 'database.db'


def db_init():
    # file, result, satisfied, rating, reason, feedback
    con = sqlite3.connect(database_path)
    cur = con.cursor()
    query = """
        CREATE TABLE IF NOT EXISTS user (
            id integer primary key AUTOINCREMENT,
            email varchar(30),
            role varchar(15),
            password varchar(50)
            );
        CREATE TABLE IF NOT EXISTS sas_training (
            id integer primary key AUTOINCREMENT,
            file varchar(50),
            result,
            rating integer,
            reason,
            uploader_id INTEGER NOT NULL,
            FOREIGN KEY (uploader_id) REFERENCES user (id)
            );
        CREATE TABLE IF NOT EXISTS nonsas_training (
            id integer primary key AUTOINCREMENT,
            file varchar(50),
            result,
            saved BIT,
            retrained BIT,
            rating integer,
            reason,
            feedback,
            uploader_id INTEGER NOT NULL,
            FOREIGN KEY (uploader_id) REFERENCES user (id)
            );
        """
    cur.executescript(query)


def get_user_by_email(email):
    con = sqlite3.connect(database_path)
    cur = con.cursor()
    query = "SELECT * FROM user WHERE email = '{}'".format(
        email)
    user = cur.execute(query).fetchone()
    return user


def user_login(userInfo):
    user = get_user_by_email(userInfo['email'])
    if user != None and user[3] == userInfo['password']:
        return user


def user_register(userInfo):
    user = get_user_by_email(userInfo['email'])
    if user == None:
        con = sqlite3.connect(database_path)
        cur = con.cursor()
        cur.execute("""
        INSERT INTO user (email, password, role) VALUES
            ('{}', '{}', '{}')
        """.format(userInfo['email'], userInfo['password'], userInfo['role']))
        con.commit()
        return get_user_by_email(userInfo['email'])


def submitSatisfied(data):
    con = sqlite3.connect(database_path)
    cur = con.cursor()
    query = """
        INSERT INTO sas_training (file, result, rating, reason, uploader_id) VALUES
            ('{}', '{}', '{}', '{}', {})
    """.format(data['file'], data['result'], data['rating'], data['reason'], data['userId'])
    cur.execute(query)
    con.commit()
    return True


def submitUnSatisfied(data):
    con = sqlite3.connect(database_path)
    cur = con.cursor()
    query = """
        INSERT INTO nonsas_training (file, result, saved, retrained, rating, reason, feedback) VALUES
            ('{}', '{}', 0, 0, '{}', '{}', '{}')
    """.format(data['file'], data['result'], data['rating'], data['reason'], data['feedback'])
    cur.execute(query)
    con.commit()
    return True


def getUserById(id):
    con = sqlite3.connect(database_path)
    cur = con.cursor()
    query = "SELECT * FROM user WHERE id = {}".format(
        id)
    user = cur.execute(query).fetchone()
    return user


def getAllUnsatisfied():
    con = sqlite3.connect(database_path)
    cur = con.cursor()
    query = """
        SELECT * from nonsas_training where retrained = 0
    """
    return fetch_dict_result(cur.execute(query))


def saveTrainingResult(id, result):
    con = sqlite3.connect(database_path)
    cur = con.cursor()
    query = """
        UPDATE nonsas_training SET result = '{}', saved = 1 where id = {}
    """.format(result, id)
    cur.execute(query)
    con.commit()
    return True


def retrain_model():
    con = sqlite3.connect(database_path)
    cur = con.cursor()
    query = """
        UPDATE nonsas_training SET retrained = 1 where saved = 1
    """
    cur.execute(query)
    con.commit()
    return True
