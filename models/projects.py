from datetime import datetime
from flask import g

db = g.db

# /users/<id>/projects/<id>
class Project(db.Model):
    __tablename__ = "projects"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    stations = db.relationship("Station", backref="station")

    name = db.Column(db.String(64), nullable=False, unique=True)
    length_overall = db.Column(db.Float(precision=4), nullable=False)
    length_perpendiculars = db.Column(db.Float(precision=4), nullable=False)
    breadth = db.Column(db.Float(precision=4), nullable=False)
    draft = db.Column(db.Float(precision=4), nullable=False)

    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updatedAt = db.Column(db.DateTime, onupdate=datetime.now)

    def __repr__(self):
        return f"<Project {self.name}>"
