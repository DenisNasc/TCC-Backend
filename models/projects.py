from datetime import datetime
from flask import g

db = g.db

# /users/<id>/projects/<id>
class Project(db.Model):
    __tablename__ = "projects"
    id = db.Column(db.String(64), primary_key=True)
    userID = db.Column(db.String(64), db.ForeignKey("users.id"), nullable=False)
    stations = db.relationship("Station", backref="station")

    name = db.Column(db.String(64), nullable=False, unique=True)
    engineer = db.Column(db.String(64), nullable=True, unique=False)
    shipyard = db.Column(db.String(64), nullable=True, unique=False)

    lengthOverall = db.Column(db.Float(precision=4), nullable=False)
    lengthPerpendiculars = db.Column(db.Float(precision=4), nullable=False)
    breadth = db.Column(db.Float(precision=4), nullable=False)
    draft = db.Column(db.Float(precision=4), nullable=False)

    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updatedAt = db.Column(db.DateTime, onupdate=datetime.now)

    def __repr__(self):
        return f"<Project {self.name}>"
