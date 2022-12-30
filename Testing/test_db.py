import sqlite3

try:

    #TODO REMAKE BLOG_LIKE AND BLOG_FAV MAKE USER_FOLLOW

    conn = sqlite3.connect('test.db')

    cursor = conn.cursor()
    print("Connecting to database")

    query = "INSERT INTO user_info VALUES (4, 'John', 'John')"
    cursor.execute(query)


    query = "INSERT INTO blog_info VALUES (4, 'John''s First Blog', 1, 'This is John''s First Blog')"
    cursor.execute(query)
    
    query = "INSERT INTO blog_like VALUES (1, 1)"
    cursor.execute(query)
    
    query = "SELECT * FROM blog_like"
    cursor.execute(query)
    result = cursor.fetchall()
    print(result)
    
    query = "SELECT * FROM blog_info"
    cursor.execute(query)
    result = cursor.fetchall()
    print(result)
    
    query = "SELECT * FROM user_info"
    cursor.execute(query)
    result = cursor.fetchall()
    print(result)
    #hmmmmmm wow new change


except Exception as e:

    print(e)

finally:

    conn.commit()
    conn.close()