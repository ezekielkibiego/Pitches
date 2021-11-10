from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Post(db.Model):
    _tablename_ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    category = db.Column(db.String)
    content = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comment = db.relationship('Comment', backref='post', lazy='dynamic')
    upvote = db.relationship('Upvote',backref='post',lazy='dynamic')
    downvote = db.relationship('Downvote',backref='post',lazy='dynamic')

    def save_post(self):
        db.session.add(self)
        db.session.commit()

    def _repr_(self):
        return f'Post {self.title}'


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
    

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls, post_id):
        comments = Comment.query.filter_by(post_id=post_id).all()
        return comments

    @classmethod
    def get_comment_author(cls, user_id):
        author = User.query.filter_by(id=user_id).first()

        return author


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    post = db.relationship('Post', backref='user', lazy="dynamic")

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, index=True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pass_secure = db.Column(db.String(255))

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.pass_secure, password)

    def __repr__(self):
        return f'User {self.username}'


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    picture_path = db.Column(db.String(64))

    @staticmethod
    def get_all_category():
        return Category.query.all()

    def save_category(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<Category %r>' % self.name


class Upvote(db.Model):
    _tablename_ = 'upvotes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_upvotes(cls, id):
        upvote = Upvote.query.filter_by(post_id=id).all()
        return upvote

    def _repr_(self):
        return f'{self.user_id}:{self.post_id}'


class Downvote(db.Model):
    _tablename_ = 'downvotes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_downvotes(cls, id):
        downvote = Downvote.query.filter_by(post_id=id).all()
        return downvote

    def _repr_(self):
        return f'{self.user_id}:{self.post_id}'
