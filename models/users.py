from datetime import datetime
from flask import g

db = g.db

# /users/<id>
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(64), unique=True, nullable=False, primary_key=True)
    
    projects = db.relationship("Project", backref="user")

    name = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(72), nullable=False)

    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updatedAt = db.Column(db.DateTime, onupdate=datetime.now)

    def __repr__(self):
        return f"<User {self.name}>"
