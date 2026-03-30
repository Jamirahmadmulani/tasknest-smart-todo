from app import db, login_manager
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))

    tasks = db.relationship("Task", backref="user", lazy=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
