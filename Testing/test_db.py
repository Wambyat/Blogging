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

a = sql_query("user_info","name")

if type("abc") == type(a):
    print (a)

else:
    a = [j for i in a for j in i]
    print(a)
    if "John" in a:
        print("John is in the list")