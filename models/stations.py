from enum import Enum
from datetime import datetime
from flask import g

db = g.db


class EnumType(Enum):
    none: 0
    deck: 1
    chine: 2


# /users/<user_id>/projects/<project_id>/stations/<id>
class Station(db.Model):
    __tablename__ = "stations"
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)

    type = db.Column(db.Enum(EnumType), default=0)
    vertical = db.Column(db.Float(precision=4))
    transversal = db.Column(db.Float(precision=4))

    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updatedAt = db.Column(db.DateTime, onupdate=datetime.now)

    def __repr__(self):
        return f"<Station {self.name}>"