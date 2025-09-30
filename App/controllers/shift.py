from App.models import Shift
from App.database import db

def create_shift(user_id, start_time, end_time, date):
    newshift = Shift(user_id=user_id, start_time=start_time, end_time=end_time, date=date)
    db.session.add(newshift)
    db.session.commit()
    return newshift

def get_shift(shift_id):
    return db.session.get(Shift, shift_id)   

def get_shifts_by_user(user_id):
    return db.session.scalars(db.select(Shift).filter_by(user_id=user_id)).all()

def get_shifts_by_date(target_date):
    return db.session.scalars(db.select(Shift).filter_by(date=target_date)).all()

def get_shifts_between(start_date, end_date):
    return db.session.scalars(db.select(Shift).filter(Shift.date >= start_date).filter(Shift.date <= end_date)).all()


def get_all_shifts():
    return db.session.scalars(db.select(Shift)).all()

def clock_in(shift_id):

    shift = Shift.query.get(int(shift_id))

    if shift:
        shift.clock_in()
        db.session.commit()
        print(f"Clocked in at {shift.time_in}")
    else:
        print("Shift not found!")

def clock_out(shift_id):

    shift = Shift.query.get(int(shift_id))
    if shift:
        shift.clock_out()
        db.session.commit()
        print(f"Clocked out at {shift.time_out}")
    else:
        print("Shift not found!")
    
