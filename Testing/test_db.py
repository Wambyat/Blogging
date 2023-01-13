import sqlite3

#* This is the file with all the created sql functions
#* They return a list of sets so we need to reformat after we call the function. 
#* Output: [(),(),() .... ]



#This returns the entire column from a table mainly used in login, signup, and password reset
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

#This returns the result of the given query.
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