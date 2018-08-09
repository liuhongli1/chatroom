import pymysql
import re
conn = pymysql.connect('localhost','root','123456','chat_room')
cursor=conn.cursor()
def enter_fun(name,password):
    cursor.execute('select name from users;')
    name1=(name,)
    if name1 in cursor.fetchall():
        return 'W'#返回注模块w为名字存在
    else:
        try:
            cursor.execute("insert into users (name,password) values\
                ('%s','%s')"%(name,password))
            conn.commit()
            return 'OK'#名字正常使用
        except:
            conn.rollback()
            return 'FALL'

    cursor.close()
    conn.close()
def login_fun(name,password):
    cursor.execute("select password from users where name='%s'"%name)
    l=cursor.fetchone()
    if l:
        if l[0]==password:
            return 0
    else:
        return 1
def seek_anyone():
    cursor.execute("select name from users")
    tuple1=cursor.fetchall()
    Str=''
    for tp in tuple1:
        Str += ' '+tp[0]
    return tuple1
def save_info_fun(name,rece_name,info):
    sql="insert into history (name,rece_name,info) values('%s','%s','%s')"%(name,rece_name,info)
    cursor.execute(sql)
    conn.commit()

def seek_fun(data=0):
    if data==0:
        cursor.execute("select * from history")
        tuble=cursor.fetchall()
    else:
        print(type(data))
        data=int(data)
        cursor.execute("select * from history limit '%d'"%data)
        tuble=cursor.fetchall()
    return tuble#返回一个列表 包含所有由每条信息组成的字典

def seek_name_fun(name,data=0):
    if data==0:
        cursor.execute("select * from history where name='%s'"%name)
        tuble=cursor.fetchall()
    else:
        print(type(data))
        print(data)
        data=int(data)
        sql="select * from history where name='%s' limit %d"%(name,data)
        cursor.execute(sql)
        tuble=cursor.fetchall()
    return tuble
def seek_rece_name_fun(name,rece_name,data=0):
    if data==0:
        cursor.execute("select * from history \
            where name='%s' and rece_name='%s'"%(name,rece_name))
        tuble=cursor.fetchall()
    else:
        print(type(data))
        data=int(data)
        cursor.execute("select * from history \
            where name='%s' and rece_name='%s' limit %d"%(name,rece_name,data))
        tuble=cursor.fetchall()
    return tuble

# print(seek_fun('liuhongli','china'))