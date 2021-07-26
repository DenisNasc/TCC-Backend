from datetime import datetime
from flask import g

db = g.db


# /users/<user_id>/projects/<project_id>/stations/<station_id>/coordinates
class Coordinates(db.Model):
    __tablename__ = "coordinates"
    id = db.Column(db.String(64), primary_key=True)
    userID = db.Column(db.String, db.ForeignKey("users.id"), nullable=False)
    projectID = db.Column(db.String, db.ForeignKey("projects.id"), nullable=False)
    stationID = db.Column(db.String, db.ForeignKey("stations.id"), nullable=False)

    type = db.Column(db.String(12), nullable=True)
    vertical = db.Column(db.Float(precision=4))
    transversal = db.Column(db.Float(precision=4))

    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updatedAt = db.Column(db.DateTime, onupdate=datetime.now)

    def __repr__(self):
        return f"<Station {self.name}>"
