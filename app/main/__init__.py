from flask import Blueprint 

main_bp = Blueprint("main",__name__) # __name__ == 路徑名稱
from . import views
# 多加了一行 from . import views，這樣他才會被好好 register 進 app。