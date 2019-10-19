from datetime import datetime

from flask import render_template, redirect, flash, url_for, request,current_app
from flask_login import current_user, login_required


from app.forms import PostForm, EditProfileForm
from app import db
from app.models import User,Post
from app.main import bp



@bp.route('/',methods=['GET','POST'])
@bp.route('/index',methods=['GET','POST'])
@login_required
def index():
    form=PostForm()
    if form.validate_on_submit():
        # 将博文保存到数据库中
        post=Post(body=form.post.data,author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('main.index'))

    page = request.args.get('page', 1, type=int)
    # 从数据库中查询出所有自己的博文以及关注用户的博文
    # posts = current_user.followed_posts().all()
    posts=current_user.followed_posts().paginate(page,current_app.config['POSTS_PER_PAGE'],False)  #False超过范围不报错
    next_url = url_for('main.index', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.index', page=posts.prev_num) if posts.has_prev else None
    # 模板文件
    return render_template('index.html',title='Home',form=form,posts=posts.items, next_url=next_url, prev_url=prev_url)

@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    # 查出所有的博文
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.explore', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.explore', page=posts.prev_num) if posts.has_prev else None
    # posts.items才是数据
    return render_template('index.html', title='Explore', posts=posts.items, next_url=next_url, prev_url=prev_url)


@bp.route('/user/<username>')
@login_required
def user(username):
    user=User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.user', username=user.username, page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.user', username=user.username, page=posts.prev_num) if posts.has_prev else None
    return render_template('user.html', user=user, posts=posts.items, next_url=next_url, prev_url=prev_url)


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@bp.route('/edit_profile',methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm(original_username=current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')      # 闪现消息
        return redirect(url_for('main.edit_profile',username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)


@bp.route('/follow/<username>')
@login_required
def follow(username):
    user=User.query.filter_by(username=username).first()
    if user is None:
        flash( "User"+username+'is not exsit')
        return redirect(url_for('main.index',username=username))
    # 是不是自己
    if user == current_user:
        flash('Can not follow yourself')
        return redirect(url_for('main.user', username=username))
    # 关注的操作
    current_user.follow(user)
    db.session.commit()
    flash('Followed Successfully')
    return redirect(url_for('main.user', username=username))

@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user=User.query.filter_by(username=username).first()
    if user is None:
        flash( "User"+username+'is not exsit')
        return redirect(url_for('main.index',username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('Unfollowed Successfully')
    return redirect(url_for('main.user',username=username))


