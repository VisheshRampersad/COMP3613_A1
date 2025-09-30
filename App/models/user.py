from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    role = db.Column(db.String(20), nullable=False, default='staff')
    #is_active = db.Column(db.Boolean, nullable =False, default=True)
    
    shifts = db.relationship('Shift', backref='user', lazy=True)


    def __init__(self, username, password, email=None , role='staff'):
        self.username = username
        self.set_password(password)

        if not email:
            self.email = f"{username}@test.com"
        else:
            self.email = email

        self.role = role

    def get_json(self):

        return {
            'id': self.id, 'username': self.username
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
    
    def is_admin(self):
        return self.role == 'admin'


#functions in app/controllers/user.py
