import sqlite3

def sql_query(tbl , col):
    
    try:
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()
        
        print("\nConnecting to database\n")

        query = "SELECT "+str(col)+" FROM "+str(tbl)
        cursor.execute(query)
        result = cursor.fetchall()
        
    except Exception as e:

        result = "Error"

    finally:

        conn.commit()
        conn.close()
        print("\nConnection closed\n")
        return result

def sql_dir(query1):

    try:
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()
        
        print("\nConnecting to database nyan\n")

        cursor.execute(query1)
        result = cursor.fetchall()
        
    except Exception as e:

        result = "Error"

    finally:

        conn.commit()
        conn.close()
        print("\nConnection closed\n")

        return result

curr_user = 1
query1 = "SELECT * FROM blog_info WHERE uid IN (SELECT user_id FROM user_follow WHERE follower_id  = "+str(curr_user)+")"
temp = sql_dir(query1)
res=[]
for i in temp:
    res.append([j for j in i])

for i in res:
    print(i[1])
    print(i[3])