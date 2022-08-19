from . import admin_bp
from ..database.helper import *
from ..forms import *
from flask import flash , render_template , redirect , url_for , request , make_response , abort
from datetime import datetime



@admin_bp.route("/admin_dashboard/posts",methods=["GET","POST"])
def admin_dashboard_posts_page():
    '''
        管理員的貼文篩選器
        可用start,end,user_id進行篩選
    '''
    filter_args = {}
    if start := request.cookies.get("start"):
        filter_args["start"] = datetime.strptime(start,"%Y-%m-%d")
    if end := request.cookies.get("end"):
        filter_args["end"] = datetime.strptime(end,"%Y-%m-%d") 
    if user_id := request.cookies.get("user_id"):
        filter_args["user_id"] = user_id
    form = AdminDashboardFilter(**filter_args)
    
    if request.method == "GET":
        posts = get_posts(**filter_args)
        return render_template("admin_dashboard_posts.html",posts=posts,form=form)
    if request.method == "POST":
        response = make_response(redirect(url_for("admin.admin_dashboard_posts_page")))
        if form.validate_on_submit():
            cookies = []
            if form.start.data:
                cookies.append(("start",form.start.data.strftime("%Y-%m-%d")))
            if form.end.data:
                cookies.append(("end",form.end.data.strftime("%Y-%m-%d")))
            if form.user_id.data:
                cookies.append(("user_id"),str(form.user_id.data)) # 要轉字串 不然會報錯
            
            response.delete_cookie("start")
            response.delete_cookie("end")
            response.delete_cookie("user_id")
            for cookie in cookies:
                response.set_cookie(*cookie)
        else:
            for field,errors in form.errors.items():
                for error in errors:
                    flash(error,category="alert")
        return response




@admin_bp.route("/admin_dashboard/comments",methods=["GET","POST"])
def admin_dashboard_comments_page():
    '''
        管理員的留言篩選器
        用start,end,user_id進行篩選
    '''
    filter_args = {}
    if start := request.cookies.get("start"):
        filter_args["start"] = datetime.strptime(start,"%Y-%m-%d")
    if end := request.cookies.get("end"):
        filter_args["end"] = datetime.strptime(end,"%Y-%m-%d") 
    if user_id := request.cookies.get("user_id"):
        filter_args["user_id"] = user_id
    form = AdminDashboardFilter(**filter_args)
    
    if request.method == "GET":
        posts = get_all_comments(**filter_args)
        return render_template("admin_dashboard_comments.html",posts=posts,form=form)
    if request.method == "POST":
        response = make_response(redirect(url_for("admin.admin_dashboard_comments_page")))
        if form.validate_on_submit():
            cookies = []
            if form.start.data:
                cookies.append(("start",form.start.data.strftime("%Y-%m-%d")))
            if form.end.data:
                cookies.append(("end",form.end.data.strftime("%Y-%m-%d")))
            if form.user_id.data:
                cookies.append(("user_id"),str(form.user_id.data)) # 要轉字串 不然會報錯
            
            response.delete_cookie("start")
            response.delete_cookie("end")
            response.delete_cookie("user_id")
            for cookie in cookies:
                response.set_cookie(*cookie)
        else:
            for field,errors in form.errors.items():
                for error in errors:
                    flash(error,category="alert")
        return response




@admin_bp.route("/manage_user",methods=["GET","POST"])
def manage_user_page():
    '''
        管理員的user篩選器
        用start,end,user_id,username進行篩選
    '''
    filter_args = {}
    if start := request.cookies.get("start"):
        filter_args["start"] = datetime.strptime(start,"%Y-%m-%d")
    if end := request.cookies.get("end"):
        filter_args["end"] = datetime.strptime(end,"%Y-%m-%d") 
    if user_id := request.cookies.get("user_id"):
        filter_args["user_id"] = user_id
    if username := request.cookies.get("username"):
        filter_args["username"] = username
    form = UserFilterForm(**filter_args)
    
    if request.method == "GET":
        posts = get_all_users(**filter_args)
        return render_template("manage_user.html",posts=posts,form=form)
    if request.method == "POST":
        response = make_response(redirect(url_for("admin.manage_user_page")))
        if form.validate_on_submit():
            cookies = []
            if form.start.data:
                cookies.append(("start",form.start.data.strftime("%Y-%m-%d")))
            if form.end.data:
                cookies.append(("end",form.end.data.strftime("%Y-%m-%d")))
            if form.user_id.data:
                cookies.append(("user_id"),str(form.user_id.data)) # 要轉字串 不然會報錯
            if form.username.data:
                cookies.append(("username",form.username.data))
            
            response.delete_cookie("start")
            response.delete_cookie("end")
            response.delete_cookie("user_id")
            response.delete_cookie("username")
            for cookie in cookies:
                response.set_cookie(*cookie)
        else:
            for field,errors in form.errors.items():
                for error in errors:
                    flash(error,category="alert")
        return response




@admin_bp.route("/admin_dashboard_posts_backend",methods=["DElETE"])
def admin_dashboard_posts_backend():
    data = request.get_json(force=True)
    post_id = data["post_id"]
    try:
        delete_post_admin(post_id)
        return "OK"
    except:
        abort(400)    



@admin_bp.route("/admin_dashboard_comments_backend",methods=["DELETE"])
def admin_dashboard_comments_backend():
    data = request.get_json(force=True)
    comment_id = data["comment_id"]
    try:
        delete_comment_admin(comment_id)
        return "OK"
    except:
        abort(400)
    # request 並用了他的 get_json 函式。這邊加了一個 force=True，
    # 是因為 flask 會偵測 request 的 MIME type，
    # 如果不是 JSON 他就會不讓你 parse，
    # 加了這個參數之後他不管如何就是會 parse，
    # 但如果內容不是 JSON 的話他還是會噴錯誤



@admin_bp.route("/manage_user_backend",methods=["PATCH","DELETE"])
def manage_user_backend():
    if request.method == "PATCH":
        data = request.get_json(force=True)
        if(update_user_data(data["user_id"],email=data["email"],is_admin=data["is_admin"])==True):
            return "OK"
        else:
            abort(400)
    
    if request.method == "DELETE":
        data = request.get_json(force=True)
        user_id = data["user_id"]
        try:
            delete_user(user_id)
            return "OK"
        except:
            abort(400) 

