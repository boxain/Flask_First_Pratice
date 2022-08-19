from datetime import datetime
from flask import flash , redirect , url_for , request , render_template , make_response
from flask_login import login_required , current_user , login_user , logout_user
from app.database.helper import *
from app.forms import *
from . import user_bp
# 少一個顯示自己貼文的route，也把修改和刪除的route連結放在該html裡
# username_posts 也需要連結去使用，可放在dashboard和posts裡
# 設計成點擊username 就可查看該user的所有貼文
# /comments 設計在登入後，查看自己留過的言

@user_bp.route("/login",methods=["GET","POST"])
def login_page():
    '''
        若已登入會跳轉至/dashboard
        未登入則到login.html
    '''
    if current_user.is_active:
        flash("You have logined.", category="info")
        return redirect(url_for("user.dashboard_page"))
    else:
        form = LoginForm()
        if request.method == "GET":
            return render_template("login.html",form=form)
        if request.method == "POST":
            if form.validate_on_submit(): # 在form設定的驗證
                username = form.username.data
                password = form.password.data
                if user:= login_auth(username,password):
                    login_user(user)
                    flash(f"Login as {username}",category="success")
                    return redirect(url_for("user.dashboard_page"))
                else:
                    flash("Wrong username or password.",category="alert")
                    return redirect(url_for("user.login_page"))
            else:
                for field,errors in form.errors.items(): # 前者為錯誤欄位，後者為錯誤內容
                    for error in errors:
                        flash(error,category="alert")
                return redirect(url_for("user.login_page"))




@user_bp.route("/logout",methods=["GET"])
def logout_page():
    '''
        登出後跳轉至首頁
    '''
    logout_user()
    return redirect(url_for("main.index_page"))




@user_bp.route("/register",methods=["GET","POST"])
def register_page():
    '''
        若已登入則跳轉至dashboard_page
        若未登入則導到register.html
        註冊成功後跳轉至login_page
        註冊失敗則繼續停留
    '''
    if current_user.is_active:
        flash("You have logined",category="info")
        return redirect(url_for("user.dashboard_page"))
    else :
        form = RegisterForm()
        if request.method == "GET":
            return render_template("register.html",form=form)
        if request.method == "POST":
            if form.validate_on_submit():
                username = form.username.data
                password = form.password.data
                email = form.email.data
                if add_user(username,password,email):
                    flash("Register successfully.",category="success")
                    return redirect(url_for("user.login_page"))
                else:
                    flash("The username or the email has been used.",category="alert")
                    return redirect(url_for("user.register_page"))
            else:
                for field,errors in form.errors.items():
                    for error in errors:
                        flash(error,category="alert")
                return redirect(url_for("user.register_page"))




@user_bp.route("/setting",methods=["GET","POST"])
@login_required
def user_setting_page():
    '''
        GET : 回傳user_setting.html
        POST : 回傳user_setting.html
    '''
    data = render_user_data(current_user.id)
    form = UserSettingForm(email=data["email"]) # 讓 email 直接顯示在前端
    if request.method == "GET":
        return render_template("user_setting.html",form=form)
    if request.method == "POST":
        if form.validate_on_submit():
            password = form.password.data
            email = form.email.data
            if(msg:=update_user_data(current_user.id,password=password,email=email)):
                flash("OK",category="success")
            else:
                flash(msg,category="alert")
        else:
            for field , errors in form.errors.items():
                for error in errors:
                    flash(error,category="alert")
        return redirect(url_for("user.user_setting_page"))




@user_bp.route("/post/add",methods=["GET","POST"])
@login_required
def add_post_page():
    '''
    GET : 回傳write.html
    POST : url_for(dashboard_page/add_post_page)
    '''
    form = AddPostForm()
    if request.method == "GET":
        return render_template("write.html",form=form,route="/post/add")
    if request.method == "POST":
        if form.validate_on_submit():
            title = form.title.data
            description = form.description.data
            content = form.content.data
            if add_post(current_user.id , title , description , content):
                flash("Add post.")
                return redirect(url_for("user.your_posts"))
            else:
                flash("The title has been used")
                return redirect(url_for("user.your_posts"))
        else:
            for field,errors in form.errors.items():
                for error in errors:
                    flash(error,category="alert")
            return redirect(url_for("user.your_posts"))



@user_bp.route("/post/edit/<int:post_id>",methods=["GET","POST"])
@login_required
def edit_post_page(post_id):
    '''
        GET : 回傳 write.html
        POST : url_for(dashboard_page/edit_post_page)
    '''
    post_data = render_post(post_id)
    form = AddPostForm(
        title = post_data["title"],
        description = post_data["description"],
        content = post_data["content"]
    )
    if request.method == "GET":
        return render_template("write.html",form=form,route=f"/post/edit/{post_id}")
    if request.method == "POST":
        if form.validate_on_submit():
            title = form.title.data
            description = form.title.data
            content = form.content.data
            print(title)
            if edit_post(post_id,title,description,content):
                flash("Post edited.")
                return redirect(url_for("user.your_posts"))
            else:
                flash("The title has been used.")
                return redirect(url_for("user.edit_post_page", post_id=post_id)) # 要加Id
        else:
            for field,errors in form.errors.items():
                for error in errors:
                    flash(error,category="alert")
            return redirect(url_for("user.edit_post_page" , post_id=post_id)) # 可能要加Id




@user_bp.route("/dashboard",methods=["GET","POST"])
@login_required
def dashboard_page():
    '''
        篩選器
    '''
    filter_args = {}
    if start := request.cookies.get("start"):
        filter_args["start"] = datetime.strptime(start,"%Y-%m-%d")
    if end := request.cookies.get("end"):
        filter_args["end"] = datetime.strptime(end,"%Y-%m-%d")
    form = DashboardFilterForm(**filter_args) # 原來還能傳dict
    if request.method == "GET":
        posts = get_posts(user_id=None , **filter_args)
        return render_template("dashboard.html",posts=posts,form=form)
    if request.method == "POST":
        response = make_response(redirect(url_for("user.dashboard_page"))) # 回傳模板
        if form.validate_on_submit():
            cookies = [] # 內容物為元組
            if form.start.data:
                cookies.append(("start",form.start.data.strftime("%Y-%m-%d")))
            if form.end.data:
                cookies.append(("end",form.end.data.strftime("%Y-%m-%d")))
            response.delete_cookie("start") # 刪除cookies
            response.delete_cookie("end") # 刪除cookies
            for cookie in cookies:
                response.set_cookie(*cookie) # 重新加入新cookies
        else:
            for field,errors in form.errors.items():
                for error in errors:
                    flash(error,category="alert")
        return response




@user_bp.route("/post/delete/<int:post_id>",methods=["GET"])
@login_required
def delete_post_page(post_id):
    if delete_post(current_user.id , post_id):
        flash("OK.")
    else:
        flash("failed.")
    return redirect(url_for("user.your_posts"))



@user_bp.route("/posts",methods=["GET"])
@login_required
def all_posts_page():
    '''
    顯示所有貼文
    '''
    posts = get_posts()
    return render_template("posts.html",posts=posts)



@user_bp.route("/@<username>/posts" , methods=["GET"])
@login_required
def user_posts_page(username):
    '''
        可得某個user的所有貼文
    '''
    user = get_user_by_username(username)
    posts = get_posts(user['id'])
    return render_template("posts.html",posts=posts)



@user_bp.route("/your/posts" , methods=["GET"])
@login_required
def your_posts():
    '''
        獲得登入者的所有貼文
    '''
    posts = get_posts(current_user.id)
    return render_template("your_posts.html",posts=posts)



@user_bp.route("/post/<int:post_id>",methods=["GET","POST"])
@login_required
def view_post_page(post_id):
    '''
        GET : 查看單一貼文內容與貼文留言
        POST : 新增留言 
    '''
    form = AddCommentForm()
    if request.method == "GET":
        post = render_post(post_id)
        comments = get_comments(post_id)
        return render_template("post.html",post=post,comments=comments,form=form)
    if request.method == "POST":
        if form.validate_on_submit():
            add_comment(current_user.id , post_id , form.content.data)        
        else:
            for field,errors in form.errors.items():
                for error in errors:
                    flash(error)
                      
        return redirect(url_for("user.view_post_page",post_id=post_id))



@user_bp.route("/comments",methods=["GET"])
@login_required
def comments_dashboard_page():
    '''
        查看使用者留過的言
        以及留言的貼文，並附帶連結
    '''
    comments = get_user_comments(current_user.id)
    return render_template("comments.html",comments=comments)




