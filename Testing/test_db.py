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

#######################################
#*           SEARCH FUNCTION         #
#* returns a dictionary with 2 lists {user:[],blog:[]}

def search_func(term):
    query_blog = "SELECT bid, btitle, bcontent, name FROM blog_info JOIN user_info on uid = id WHERE btitle LIKE '%"+term+"%';"

    query_user = "SELECT name,description FROM user_info JOIN user_addi on id = uuid WHERE name LIKE '%"+term+"%';"

    user_res = sql_dir(query_user)
    blog_res = sql_dir(query_blog)

    user_res = [list(i) for i in user_res]
    blog_res = [list(i) for i in blog_res]

    return {"user":user_res,"blog":blog_res}


#######################################
#*          New Blog Function        #

def new_blog(title,content,uid):


    temp = sql_query("blog_info","bid")
    temp = [int(i) for j in temp for i in j]
    blog_id = max(temp)+1
    query = "INSERT INTO blog_info VALUES ("+str(blog_id)+",'"+title+"',"+str(uid)+",'"+content+"')"
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    conn.close()
    return blog_id

def same_user(blogID, cid):

    query = "SELECT uid FROM blog_info WHERE bid ="+str(blogID)
    res = sql_dir(query)
    res = [j for i in res for j in i]
    print(res)

    if res == []:
        return "b"

    uid = res[0]
    if int(uid) == int(cid):
        print("here")
        return "a"
    else:

        print("HOW THE FUCK")
        return "b"

def update_blog(blogID, title, content):

    query = "UPDATE blog_info SET btitle = '"+title+"', bcontent = '"+content+"' WHERE bid = "+str(blogID)
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    conn.close()

def delete_blog(blogID):
    
    query = "DELETE FROM blog_info WHERE bid = "+str(blogID)
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    conn.close()