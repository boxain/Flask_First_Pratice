from flask import current_app # 用來取得 

def get_url_app():
    print(current_app.url_map)