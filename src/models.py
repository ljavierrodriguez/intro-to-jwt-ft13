from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Intent(db.Model):
    __tablename__ = 'intents'
    username = db.Column(db.String(150), unique=True, primary_key=True)
    intent = db.Column(db.Integer, default=1)

    def serialize(self):
        return {
            "username": self.username,
            "intent": self.intent
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    isActive = db.Column(db.Boolean, default=True)

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "isActive": self.isActive
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


