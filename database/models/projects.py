from datetime import datetime
from flask import g

db = g.db


class ProjectModel(db.Model):
    __tablename__ = "projects"
    id = db.Column(db.String(64), primary_key=True)
    userID = db.Column(db.String(64), db.ForeignKey("users.id"), nullable=False)

    stations = db.relationship("StationModel", backref="station")

    name = db.Column(db.String(64), nullable=False, unique=True)
    engineer = db.Column(db.String(64), nullable=False, unique=False)
    shipyard = db.Column(db.String(64), default="")

    lengthOverall = db.Column(db.Float(precision=4), nullable=True)
    lengthPerpendiculars = db.Column(db.Float(precision=4), nullable=True)
    breadth = db.Column(db.Float(precision=4), nullable=True)
    draft = db.Column(db.Float(precision=4), nullable=True)

    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updatedAt = db.Column(db.DateTime, onupdate=datetime.now, default=datetime.now())

    def __repr__(self):
        return f"<Project {self.name}>"
