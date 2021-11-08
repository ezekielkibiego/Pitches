from flask import render_template,request,redirect,url_for,abort, flash
from . import main
from ..models import Comment, User,Post
from flask_login import login_required, current_user
from .. import db,photos
from .forms import UpdateProfile, PostForm, CommentForm

@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data.
    '''
    post_form = PostForm()
    all_posts = Post.query.order_by(Post.date_posted).all()
    return render_template('index.html', posts = all_posts)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)
    return render_template("profile/profile.html", user = user)
@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)
    form = UpdateProfile()
    if form.validate_on_submit():
        user.bio = form.bio.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('.profile',uname=user.username))
    return render_template('profile/update.html',form =form)
@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))


@main.route('/comment', methods=['GET', 'POST'])
@login_required
def add_comment():
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(name=form.name.data)
        db.session.add(comment)
        db.session.commit()
        flash('Comment added successfully.')
        return redirect(url_for('.index'))
    return render_template('comments.html', form=form)

@main.route('/post', methods=['GET', 'POST'])
@login_required
def new_post():
    post_form = PostForm()
    if post_form.validate_on_submit():
        title = post_form.post_title.data
        category = post_form.post_category.data
        content = post_form.post_content.data
        new_post = Post(title=title, content=content, user=current_user, category=category)
        new_post.save_post()
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('main.index'))

    else:
        all_posts = Post.query.order_by(Post.date_posted).all()

    return render_template('pitches.html', posts=all_posts,post_form = post_form)
