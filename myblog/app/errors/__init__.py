# 生成蓝图对象
from flask import Blueprint
bp = Blueprint('errors', __name__)


# 导入接口文件
from app.errors import handlers
