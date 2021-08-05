from datetime import datetime
from flask import g

db = g.db


# /users/<user_id>/projects/<project_id>/stations/<id>
class StationModel(db.Model):
    __tablename__ = "stations"
    id = db.Column(db.String(64), primary_key=True)
    projectID = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)
    userID = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    coordinates = db.relationship("CoordinateModel", backref="coordinate")

    name = db.Column(db.String(64), nullable=False)
    longitudinal = db.Column(db.Float(precision=4), nullable=False)

    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updatedAt = db.Column(db.DateTime, onupdate=datetime.now)

    def __repr__(self):
        return f"<Station {self.name}>"
