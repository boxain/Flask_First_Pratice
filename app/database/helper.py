from .models import  db,Users,Posts,Comments
from ..user_helper import User
from werkzeug.security import generate_password_hash

def init():
    # 創建所有表
    db.create_all()
    

def reset():
    db.drop_all()
    db.create_all()


def add_user(username,password,email,introduction=None,is_admin=False):
    user = Users(username,password,email,introduction,is_admin)
    try :
        db.session.add(user)
        db.session.commit()
        return True
    except ValueError as v:
        print("錯誤: ",v)
        return False

# Flask_Login的判斷
def login_auth(username,password):
    if user := Users.query.filter_by(username=username).first():
        if user.check_password(password):
            sessionUser = User()
            sessionUser.id = user.id
            return sessionUser
    return False


def user_to_dict(user_objects:list):
    li = []
    for user in user_objects:
        d = dict()
        d["id"] = user.id
        d["username"] = user.username
        d["email"] = user.email
        d["is_admin"] = user.is_admin
        d["introduction"] = user.introduction
        d["register_time"] = user.register_time.strftime("%Y-%m-%d %H:%M:%S")
        li.append(d)
    return li

# 回傳使用者資訊 回傳值是user_to_dict
def render_user_data(user_id):
    if user:= Users.query.filter_by(id=user_id).first():
        return user_to_dict([user])[0]
    else:
        return False

# 利用字典形式修改資料列row
def update_user_data(user_id,password=None,email=None,is_admin=None):
    filter = Users.query.filter_by(id=user_id)
    if filter.first():
        data = {}
        if password:
            data["password"]=generate_password_hash(password)
        if email:
            data["email"]=email
        if is_admin:
            data["is_admin"] = is_admin
        try:
            filter.update(data)
            db.session.commit()
            return True
        except:
            return "Username or email is used."
    else:
        return "The user does not exist"


def add_post(user_id,title,description,content):
    post = Posts(user_id,title,description,content)
    try:
        db.session.add(post)
        db.session.commit()
        return True
    except:
        return False

# 需加上是否為作者的判斷
def edit_post(post_id , title , description , content):
    post = Posts.query.filter_by(id=post_id)
    try :
        data = {"title":title,"description":description,"content":content}
        post.update(data)
        db.session.commit()
        return True
    except:
        return False

# 回傳貼文資訊，回傳值為dict
def render_post(post_id):
    post = Posts.query.filter_by(id=post_id).first()
    return {
        "id" : post.id,
        "author_id" : post.author_id,
        "title" : post.title,
        "description" : post.description,
        "content" : post.content,
        "time" : post.time
        # "comments" : [
        #     {
        #         "author_id": comment.author_id,
        #         "content" : comment.content
        #     }
        #     for comment in post.comment
        # ]
    }


# dashboard判斷回傳貼文
def get_posts(user_id=None,start=None,end=None):
    query = Posts.query
    if user_id:
        query = query.filter_by(author_id = user_id)
    if start:
        query = query.filter(Posts.time > start)
    if end:
        query = query.filter(Posts.time < end)

    posts = [post.id for post in query.all()]
    posts = list(map(render_post,posts)) # 不知道是否與 list(render_post(post_id) for post_id in posts)一樣
    return posts
    # 有 filter 也有 filter_by，後者是我們熟悉的，而前者也一樣是篩選器，只是它裡面放的是判斷式



def delete_post(user_id,post_id):
    post = Posts.query.filter_by(id=post_id).first()
    if post.author_id == user_id:
        # db.session.delete()，裡面的參數是物件，而不是 query，所以要記得 .first()。
        db.session.delete(post)
        db.session.commit()
        return True
    else:
        return False



def get_user_by_username(username):
    user = Users.query.filter_by(username=username).first()
    return render_user_data(user.id) # 回傳User的基本Data



def add_comment(user_id,post_id,content):
    comment = Comments(author_id=user_id , post_id=post_id , content=content)
    try:
        db.session.add(comment)
        db.session.commit()
        return True
    except:
        return False

def get_comments(post_id):
    comments = Comments.query.filter_by(post_id=post_id).all()
    return [
        {
            "id": comment.id,
            "author_id": comment.author_id,
            "post_id": comment.post_id,
            "content": comment.content,
            "time":comment.time
        }
        for comment in comments
    ]



def get_user_comments(user_id):
    comments = Comments.query.filter_by(author_id=user_id).all()
    return [
        {
            "id": comment.id,
            "author_id": comment.author_id,
            "post_id": comment.post_id,
            "content": comment.content
        }
        for comment in comments
    ]



def get_all_comments(user_id=None , start=None , end=None):
    query = Comments.query
    if user_id:
        query = query.filter_by(author_id=user_id)
    if start:
        query = query.filter(Comments.time > start)
    if end:
        query = query.filter(Comments.time < end)
    return [
        {
            "id" : comment.id,
            "author_id" : comment.author_id,
            "post_id" : comment.post_id,
            "content" : comment.content,
            "time" : comment.time
        }
        for comment in query.all()
    ]



def get_all_users(user_id=None , username=None , start=None , end=None):
    
    query = Users.query
    if user_id:
        query = query.filter_by(id=user_id)
    if username:
        query = query.filter_by(username=username)
    if start:
        query = query.filter(Users.register_time > start)
    if end:
        query = query.filter(Users.register_time < end)
    return user_to_dict(query.all())


def delete_post_admin(post_id):
    post = Posts.query.filter_by(id=post_id).first() # 指定刪除貼文
    comments = Comments.query.filter_by(post_id=post_id).all() # 查詢所有欲刪除貼文的留言
    db.session.delete(post)
    for comment in comments:
        db.session.delete(post)
    db.session.commit()


def delete_comment_admin(comment_id):
    comment = Comments.query.filter_by(id=comment_id).first()
    db.session.delete(comment)
    db.session.commit()


def delete_user(user_id):
    user = Users.query.filter_by(id=user_id).first()
    posts = Posts.query.filter_by(author_id=user_id).all()
    for post in posts:
        delete_post_admin([post])
    comments = Comments.query.filter_by(author_id=user_id).all()
    for comment in comments:
        db.session.delete(comment)
    db.session.delete(user)
    db.session.commit()