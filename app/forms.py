from flask_wtf import FlaskForm
from wtforms import StringField , SubmitField , PasswordField  ,BooleanField , DateField , IntegerField
from wtforms import EmailField , HiddenField
from wtforms.validators import DataRequired , Length , EqualTo , Regexp , ValidationError , Optional
from flask_pagedown.fields import PageDownField

'''
今天我們要開始使用 Flask-WTF 來做表單，我們要做的表單還不少，
但我們每個都會實作。他的概念是用 class 的方式把表單寫起來，
然後建立一個表單實體並傳入 render_template 讓 jinja 處理。
'''

class LoginForm(FlaskForm):
    username = StringField("Username",validators=[DataRequired()],render_kw={"placeholder":"Username"})
    password = PasswordField("Password",validators=[DataRequired()],render_kw={"placeholder":"Password"})
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=4,max=30,
            message="The name should be 4 to 30 letters long."),
            Regexp("[a-zA-Z0-9_]+",
            message="Only letters, numbers and underscores are allowed in username")
        ],
        render_kw={"placeholder":"Username"}
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=6,message="The password must contain at least 6 characters."),
        ],
        render_kw={"placeholder":"Password"},
    )

    repeat_password = PasswordField(
        "Repeat Password",
        validators=[
            DataRequired(),
            EqualTo("password",message="Passwords not match."),
        ],
        render_kw={"placeholder":"Repeat Password"},
    )

    email = EmailField(
        "Email",
        validators=[DataRequired()],
        render_kw={"placeholder":"Email"}
    )
    
    submit = SubmitField("Register")


class UserSettingForm(FlaskForm):
    '''
        可更新password和email
    '''
    password = PasswordField(
        "Password",
        render_kw={"placeholder":"Password"}
    )

    email = EmailField(
        "Email",
        validators=[DataRequired()],
        render_kw={"placeholder":"Email"}
    )

    submit = SubmitField("Update")

    # 函式名稱是固定寫法
    def validate_password(self,field):
        if type(field.data) is str:
            if field.data != "" and len(field.data) < 6 :
                raise ValidationError(
                    "The password must contain at least 6 characters."
                )
        else:
            raise ValidationError("Invalid type.")


class AddUserForm(FlaskForm):
    form_name = HiddenField(render_kw={"value":"add_user"})
    username = StringField(
        "Username",
        validators=[DataRequired(),
                    Length(min=4,max=30,message="The name should be 4 to 30 letters long."),
                    Regexp("[a-zA-Z0-9_]+",message="Only letters, numbers and underscore are allowed in username.")
                    ],
        render_kw={"placeholder":"Username"}
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=6,message="The password must contain at least 6 characters.")
        ],
        render_kw={"placeholder":"Password"}
    )

    email = EmailField(
        "Email",
        validators=[
            DataRequired(),
        ],
        render_kw={"placeholder":"Email"}
    )

    is_admin = BooleanField("The user is an admin")

    submit = SubmitField("Add")


class AddPostForm(FlaskForm):
    title = StringField("Title",validators=[DataRequired()])
    description = StringField("Description")

    # PageDownField，允許我們邊編輯邊看 markdwon 長甚麼樣子
    # content = PageDownField("Enter your markdown") 
    content = StringField("Content")
    submit = SubmitField("Submit")


class AddCommentForm(FlaskForm):
    content = StringField("Comment",render_kw={"placeholder":"Cotent"})
    submit = SubmitField("Submit")


class DashboardFilterForm(FlaskForm):
    start = DateField("start",format="%Y-%m-%d" , validators=[DataRequired()])
    end = DateField("end" , format="%Y-%m-%d" , validators=[DataRequired()])
    submit = SubmitField("Submit")


class AdminDashboardFilter(FlaskForm):
    # Optional，它的功用是在這個欄位沒有被填寫的時候不要去做其他的驗證
    # 像下兩個欄位就會分別做是否是日期跟是否是整數的驗證，如果沒有 Optional 的話，就會直接被擋掉
    start = DateField("start",format="%Y-%m-%d" , validators=[Optional()])
    end = DateField("end",format="%Y-%m-%d",validators=[Optional()])
    # 沒有 render_kw 參數
    user_id = IntegerField("", validators=[Optional()] , render_kw={"placeholder":"User ID"})
    submit = SubmitField("Submit")


class UserFilterForm(FlaskForm):
    form_name = HiddenField(render_kw={"value":"filter"})
    user_id = IntegerField("User ID" , render_kw={"placeholder":"User ID"},validators=[Optional()])
    username = StringField("Username" , render_kw={"placeholder":"Username"})
    start = DateField("start",format="%Y-%m-%d" , validators=[Optional()])
    end = DateField("end",format="%Y-%m-%d" , validators=[Optional()])
    submit = SubmitField("Submit")



'''
而他的第一個參數是這個欄位的名字，後面在 jinja 那邊會用到，
他在 HTML 是 label 的角色。validators 是規定這個欄位要遵守的規則，
他是一個 list，Flask-WTF 會一一檢查，沒過就會視為無效，
到時候在寫藍圖的時候會看到怎麼判斷。
這邊使用的是 DataRequired，對應到 HTML 就是 input 裡面的 required。
而他的確會在 HTML 的部份加上 required，但就算手動把它移掉，到後端他還是會檢查一次。
最後是 render_kw，基本上它就是一些額外的參數，像此處就是指定他的 placeholder，
這樣在 HTML 那邊就會顯示出 placeholder="Username"
'''