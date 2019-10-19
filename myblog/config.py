import os
#获取当前.py文件的绝对路径
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = '#%^&gfcg#$%^xfdgh%^^U&'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG=True
    ADMINS = ['your-email@example.com']
    POSTS_PER_PAGE = 5
    # 用163需要这么写
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'LiuLei550819@163.com'   # 邮箱号
    MAIL_PASSWORD = '550819ll'  # 邮箱的授权码








