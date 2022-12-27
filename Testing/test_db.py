import sqlite3

try:
    conn = sqlite3.connect('test.db')

    cursor = conn.cursor()
    print("Connecting to database")

    '''
    query = "CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)"
    cursor.execute(query)
    '''

    query = "INSERT INTO test VALUES (1, 'John', 20)"
    cursor.execute(query)
    
    query = "SELECT * FROM test"
    cursor.execute(query)

    result = cursor.fetchall()
    print(result)
    #hmmmmmm


except Exception as e:

    print(e)

finally:

    conn.commit()
    conn.close()