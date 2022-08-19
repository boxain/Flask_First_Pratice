from functools import wraps
from flask import current_app , request , abort , flash , redirect , session
from flask_login import LoginManager , UserMixin , current_user
from .database.models import Users
from flask_login.config import USE_SESSION_FOR_NEXT
from flask_login.signals import user_unauthorized
from flask_login.utils import (
    expand_login_view,
    login_url as make_login_url,
    make_next_param,
)



# class LoginManager_(LoginManager):
#     def __init__(self):
#         super().__init__()
    
#     def forbidden(self):
#         user_unauthorized.send(current_app.get_current_object())

#         if self.unauthorized_callback:
#             return self.unauthorized_callback()

#         if request.blueprint in self.blueprint_login_views:
#             login_view = self.blueprint_login_views[request.blueprint]
#         else:
#             login_view = self.login_view

#         if not login_view:
#             abort(403)
        
#         if self.login_message:
#             if self.localize_callback is not None:
#                 flash(
#                     self.localize_callback(self.login_message),
#                     category=self.login_message_category
#                 )
#             else:
#                 flash(self.login_message,category=self.login_message_category)


#         config = current_app.config
#         if config.get("USE_SESSION_FOR_NEXT",USE_SESSION_FOR_NEXT):
#             login_url = expand_login_view(login_view)
#             session["_id"] = self._session_identifier_generator()
#             session["next"] = make_next_param(login_url,request.url)
#             redirect_url = make_login_url(login_view)
#         else:
#             redirect_url = make_login_url(login_view,next_url=request.url)
        
#         return redirect(redirect_url)


# login_manager = LoginManager_()


# def admin_required(func):
#     @wraps(func)
#     def decorated_view(*args,**kwargs):
#         if current_user.is_active:
#             if current_user.is_admin:
#                 return func(*args,**kwargs)
#             else:
#                 return login_manager.forbidden() # 限制
#         else:
#             return login_manager.unauthorized() # 未授權

login_manager = LoginManager()


class User(UserMixin):
    pass



@login_manager.user_loader
def load(user_id):
    user_id = int(user_id)
    user = Users.query.filter_by(id=user_id).first() # 符合條件的第一筆資料
    if user:
        sessionUser = User()
        sessionUser.id = user.id
        sessionUser.is_admin = user.is_admin
        return sessionUser
    else:
        return None

'''
下面的 load，他加上了一個 login_manager.user_loader 的裝飾器。
在這個函式裡面，我們去資料庫找到這個使用者，然後把它包裝一下變成剛剛定義的 User 的形式，
這樣 Flask-Login 才看得懂，而如果這個使用者不存在的話，那就回傳 None，這是官方文件指示的。
'''

