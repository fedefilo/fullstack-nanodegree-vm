#
# Database access functions for the web forum.
# 

import time
import psycopg2
import bleach



## Get posts from database.
def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''
    db = psycopg2.connect("dbname=forum") 
    c = db.cursor()
    c.execute("select content, time from posts order by time desc")
    posts = ({'content': str(row[1]), 'time': str(row[0])} 
      for row in c.fetchall())
    db.close()
    return posts

## Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
    db = psycopg2.connect("dbname=forum")
    c = db.cursor()
    t = str(time.strftime('%c', time.localtime()))
    content = bleach.clean(content)
    query = "insert into posts(time, content) values(%s, %s)"
    c.execute(query, (t, content))
    db.commit()
    db.close()
    
