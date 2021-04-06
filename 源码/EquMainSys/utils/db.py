import pymysql



def get_list(sql,args):

    conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="root" ,database="Slems",charset="utf8")
    # cursor=conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    cursor.execute(sql)
    result=cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def get_listByDic(sql,args):
    conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="root", database="Slems", charset="utf8")
    cursor=conn.cursor(cursor=pymysql.cursors.DictCursor)
    # cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def modify(sql,args):
    # try:
    conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="root", database="Slems", charset="utf8")
    # cursor=conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    return True
    # except:
        # return False
    # result = cursor.fetchall()
