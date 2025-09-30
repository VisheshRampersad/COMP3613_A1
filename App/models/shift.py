from App.database import db
from datetime import datetime

class Shift(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    date = db.Column(db.Date, nullable=False)
    time_in = db.Column(db.DateTime, nullable=True)
    time_out = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='scheduled')
    created_at = db.Column(db.DateTime, default=datetime.utcnow())

    def get_json(self):
        return {
            'id': self.id, 'user_id': self.user_id, 'username': self.user.username, 
            
            'start_time': self.start_time.strftime('%H:%M'), 'end_time': self.end_time.strftime('%H:%M'),
            'date': self.date.strftime('%Y-%m-%d'),
            
            'time_in': self.time_in.strftime('%H:%M:%S') if self.time_in else None,
            'time_out': self.time_out.strftime('%H:%M:%S') if self.time_out else None,
            
            'status': self.status
        }
    
    def clock_in(self):
        self.time_in = datetime.utcnow()
        self.status = 'in-progress'

    def clock_out(self):
        self.time_out = datetime.utcnow()
        self.status = 'completed'

#functions in app/controllers/shift.py


