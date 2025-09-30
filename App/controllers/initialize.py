from .user import *
from .shift import *
from App.database import db
from datetime import time, date, timedelta

def initialize():
    db.drop_all()
    db.create_all()
    
    #sample data to populate db
    
    admin = User(username='Boss', email='boss@test.com', role='admin', password='admin123')
    staff1 = User(username='Employee1', email='staff1@test.com', role='staff', password='staff123')
    staff2 = User(username='Employee2', email='staff2@test.com', role='staff', password='staff123')
    vishesh = User(username='Vishesh', email='vishesh@test.com', role='admin', password='vishesh123')
    
    db.session.add_all([admin, staff1, staff2, vishesh])
    db.session.commit()  
    
    today = date.today()
    
    shifts = [
        
        Shift(user_id=1, start_time=time(9, 0), end_time=time(17, 0), date=today),
        Shift(user_id=2, start_time=time(13, 0), end_time=time(21, 0), date=today),
        
        Shift(user_id=1, start_time=time(9, 0), end_time=time(17, 0), date=date(2025, 1, 15)),
        Shift(user_id=2, start_time=time(10, 0), end_time=time(18, 0), date=date(2025, 1, 15)),
        Shift(user_id=3, start_time=time(14, 0), end_time=time(22, 0), date=date(2025, 1, 16)),
        Shift(user_id=2, start_time=time(10, 0), end_time=time(18, 0), date=date(2025, 1, 16)),

        Shift(user_id=1, start_time=time(8, 0), end_time=time(16, 0), date=date(2025, 1, 17)),
        Shift(user_id=3, start_time=time(14, 0), end_time=time(22, 0), date=date(2025, 1, 17)),
        Shift(user_id=4, start_time=time(12, 0), end_time=time(20, 0), date=date(2025, 1, 18)),
        Shift(user_id=2, start_time=time(9, 30), end_time=time(17, 30), date=date(2025, 1, 19)),
        
        
        Shift(user_id=1, start_time=time(9, 0), end_time=time(17, 0), date=today + timedelta(days=1)),
        Shift(user_id=3, start_time=time(14, 0), end_time=time(22, 0), date=today + timedelta(days=1)),
        Shift(user_id=4, start_time=time(11, 0), end_time=time(19, 0), date=today + timedelta(days=2)),
    ]
    
    db.session.add_all(shifts)
    db.session.commit()