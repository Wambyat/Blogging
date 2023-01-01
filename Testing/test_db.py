import sqlite3

try:

    conn = sqlite3.connect('test.db')

    cursor = conn.cursor()
    print("\nConnecting to database\n")

    query = "SELECT sql FROM sqlite_master WHERE type='table'"
    cursor.execute(query)
    result = cursor.fetchall()
    for i in result:
        print(i)

except Exception as e:

    print(e)

finally:

    conn.commit()
    conn.close()
    print("\nConnection closed\n")