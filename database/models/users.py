from datetime import datetime
from flask import g
from flask_bcrypt import generate_password_hash, check_password_hash


db = g.db

# /users/<id>
class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(64), unique=True, nullable=False, primary_key=True)

    projects = db.relationship("ProjectModel", backref="users")

    name = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(72), nullable=False)

    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updatedAt = db.Column(db.DateTime, onupdate=datetime.now)

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode("utf8")

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"<User {self.name}>"
