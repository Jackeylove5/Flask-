# 登陆  注册  修改密码  注销（认证）
from flask import url_for, flash, request, render_template
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse
from werkzeug.utils import redirect

from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm, ResetPasswordForm, ResetPasswordRequestForm
from app.email import send_password_reset_email
from app.models import User


@bp.route('/login',methods=['GET','POST'])
def login():
    # 第一种情况就是用户已经登录
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()    # 表单实例化对象
    # form.validate_on_submit()方法完成所有表单处理工作。当浏览器发送GET接收带有表单的网页请求时，此方法将返回False，此时函数会跳过if语句并直接在函数的最后一行呈现模板。
    # 当用户在浏览器按下提交按钮时，浏览器发送POST请求，form.validate_on_submit()将收集所有数据，运行附加到字段的所有验证器，如果一切正常，它将返回True，表明数据有效且可由应用程序处理。
    # 但如果至少有一个字段未通过验证，则函数就会返回False，此时函数会跳过if语句并直接在函数的最后一行呈现模板。
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        flash('用户名：{}'.format(form.username.data))
        flash('Login seccessfully')
        # 重定向到 next 页面
        next_page=request.args.get('next')
        if not next_page or url_parse(next_page).netloc!= '':     # netloc域名
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@bp.route('/logout',methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@bp.route('/register',methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('/index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('main.index'))
    return render_template('register.html', title='Register', form=form)

# 重置密码的视图函数
@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    # 通过token进行解密  user_id 获取用户
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    # 判断用户是否存在
    if not user:
        return redirect(url_for('auth.login'))
    # 如果表单校验成功就进行重置密码的操作
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('auth.login'))
    return render_template('reset_password.html', form=form)

@bp.route('/reset_password_request', methods=['GET','POST'])
def reset_password_request():
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            # 有用户
            # 发送邮件
            send_password_reset_email(user)
            flash("'Check your email for the instructions to reset your password")
            return redirect(url_for('auth.login'))
        else:
            flash("The email is not exist,please re-enter ")
            return redirect(url_for('auth.reset_password_request'))
    return render_template('reset_password_request.html', title='Reset Password', form=form)

