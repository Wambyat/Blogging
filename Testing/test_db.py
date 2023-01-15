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


#*This checks if current user is the same as the user who created the blog additionally checks if user has liked the blog
def same_user(blogID, cid):

    query = "SELECT uid FROM blog_info WHERE bid ="+str(blogID)
    res = sql_dir(query)
    res = [j for i in res for j in i]

    if res == []:
        return "b"

    uid = res[0]
    if int(uid) == int(cid):

        return "a"

    else:

        #checks if user has liked the blog
        query = "SELECT user_id FROM blog_like WHERE user_id = "+str(cid)+" AND blog_id = "+str(blogID)
        res = sql_dir(query)
        res = [j for i in res for j in i]
        

        if res == []:

            return "b"

        else:

            return "l"

        return "b"


#This updates blog
def update_blog(blogID, title, content):

    query = "UPDATE blog_info SET btitle = '"+title+"', bcontent = '"+content+"' WHERE bid = "+str(blogID)
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    conn.close()

#This deletes blog
def delete_blog(blogID):
    
    query = "DELETE FROM blog_info WHERE bid = "+str(blogID)
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    conn.close()

#This adds a like to blog from current user
def like_blog(blogID, cid):

    query = "SELECT * FROM blog_like WHERE user_id = "+str(cid)+" AND blog_id = "+str(blogID)
    res = sql_dir(query)
    if res == []:
        query = "INSERT INTO blog_like VALUES ("+str(blogID)+","+str(cid)+")"
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        conn.close()
    else:
        query = "DELETE FROM blog_like WHERE user_id = "+str(cid)+" AND blog_id = "+str(blogID)
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        conn.close()


#This returns the number of likes for a blog
def get_likes(blogID):

    query = "SELECT user_id  FROM blog_like WHERE blog_id = "+str(blogID)
    res = sql_dir(query)
    res = [j for i in res for j in i]

    return len(res)

#This returns the number of blogs for a user
def get_blogs(uid):

    query = "SELECT bid FROM blog_info WHERE uid = "+str(uid)
    res = sql_dir(query)
    res = [j for i in res for j in i]

    return len(res)

#This returns the followers for a user
def get_followers(uid):
    
    query = "SELECT follower_id  FROM user_follow WHERE user_id = "+str(uid)
    res = sql_dir(query)
    res = [j for i in res for j in i]

    return res

#This returns followings for a user
def get_following(uid):
    
    query = "SELECT user_id FROM user_follow WHERE follower_id = "+str(uid)
    res = sql_dir(query)
    res = [j for i in res for j in i]

    return res

#This updates user_info
def update_user_info(uid,name):
    
    query = "UPDATE user_info SET name = '"+name+"' WHERE id = "+str(uid)
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    conn.close()

#This updates user_addi
def update_user_addi(uid,age,description):
    
    query = "UPDATE user_addi SET age = "+str(age)+", description = '"+description+"' WHERE uuid = "+str(uid)
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    conn.close()

#This deletes user from user_info and user_addi
def delete_user(uid):
        
    query = "DELETE FROM user_info WHERE id = "+str(uid)
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    conn.close()

    query = "DELETE FROM user_addi WHERE uuid = "+str(uid)
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    conn.close()

#This adds or removes a follower to a user
def follow_user(uid, cid):
    
    query = "SELECT * FROM user_follow WHERE user_id = "+str(uid)+" AND follower_id = "+str(cid)
    res = sql_dir(query)
    if res == []:
        query = "INSERT INTO user_follow VALUES ("+str(uid)+","+str(cid)+")"
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        conn.close()
    else:
        query = "DELETE FROM user_follow WHERE user_id = "+str(uid)+" AND follower_id = "+str(cid)
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        conn.close()

def get_user_id(username):
    query = "SELECT id FROM user_info WHERE name = '"+username+"'"
    res = sql_dir(query)
    res = [j for i in res for j in i]
    return res[0]
