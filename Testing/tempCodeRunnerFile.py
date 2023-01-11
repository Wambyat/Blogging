query1 = "SELECT * FROM blog_info WHERE uid IN (SELECT user_id FROM user_follow WHERE follower_id  = "+str(curr_user)+")"
temp = sql_dir(query1)
res=[]
for i in temp:
    res.append([j for j in i])