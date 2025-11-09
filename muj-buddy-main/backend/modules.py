from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()

class Professor(db.Model):
    __tablename__ = 'professors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    department = db.Column(db.String(120))
    email = db.Column(db.String(120))
    phone_number = db.Column(db.String(30))
    cabin_location = db.Column(db.String(120))
    block = db.Column(db.String(80))
    timetable = db.Column(db.Text)  # JSON string

    def to_dict(self):
        """Convert DB row into a dictionary."""
        try:
            tt = json.loads(self.timetable) if self.timetable else {}
        except Exception:
            tt = self.timetable or {}

        return {
            "id": self.id,
            "name": self.name,
            "department": self.department,
            "email": self.email,
            "phone_number": self.phone_number,
            "cabin_location": self.cabin_location,
            "block": self.block,
            "timetable": tt
        }

    def to_text(self):
        """Convert professor info into plain text for embeddings (used in FAISS)."""
        return (
            f"Professor {self.name} from {self.department or 'unknown department'} "
            f"can be contacted at {self.email or 'no email'} or {self.phone_number or 'no phone number'}. "
            f"Their cabin is located in {self.block or 'unknown block'}, {self.cabin_location or 'no cabin info'}. "
        )
