from App.models import User
from App.models import Shift
from App.controllers.user import *
from App.controllers.shift import *

from App.database import db
from datetime import datetime, timedelta, date

#schedule shift
def schedule(admin_id, user_id, start_time, end_time, shift_date):

    admin_id = get_user(admin_id)

    if admin_id.role != 'admin':
        print("User not admin")
        return None
    
    else:

        start = datetime.strptime(start_time, '%H:%M').time()
        end = datetime.strptime(end_time, '%H:%M').time()
        shift_date = datetime.strptime(shift_date, '%Y-%m-%d').date()
        
        shift = create_shift(user_id = user_id, start_time = start, end_time = end, date = shift_date)
        
        db.session.add(shift)
        db.session.commit()
        print(f"Shift scheduled: ID {shift.id}")

        


#view combined roster also includes for a specific week

def get_roster(start_date=None, end_date=None):

    if not start_date:
        start = date.today()

    else:
        start = datetime.strptime(start_date, '%Y-%m-%d').date()
        
    if not end_date:
        end = start + timedelta(days=6)
    else:
        end = datetime.strptime(end_date, '%Y-%m-%d').date()
    
    shifts = Shift.query.filter(Shift.date >= start, Shift.date <= end).all()
    
    print(f"\n Roster for {start} to {end}")

    print("=" * 67)

    for shift in shifts:
        user = User.query.get(shift.user_id)

        if shift.time_in: 
            time_in = shift.time_in.strftime('%H:%M')
        else:
            time_in = '--:--'
            

        if shift.time_out:
            time_out = shift.time_out.strftime('%H:%M')  
        else:
            time_out = '--:--'

            
        print(f"{shift.date} | {user.username} | {shift.start_time}-{shift.end_time} | {shift.status} | In: {time_in} | Out: {time_out}")



#weekly shift report

def report(admin_id):

    user = get_user(admin_id)

    if user.role != 'admin':
        print("User not admin")
        return None
    
    else:

        shifts = Shift.query.all()

        today = date.today()
        monday = today - timedelta(days=today.weekday())  
        friday = monday + timedelta(days=4)          
        
        

        weekly_shifts = [shift for shift in shifts if monday <= shift.date <= friday]
        
        completed = len([shift for shift in weekly_shifts if shift.status == 'completed'])
        in_progress = len([shift for shift in weekly_shifts if shift.status == 'in-progress'])
        scheduled = len([shift for shift in weekly_shifts if shift.status == 'scheduled'])
        
        print(f"\nShift Report from {monday} to {friday} \n")

        print(f"Number of Shifts: {len(shifts)}")
        print(f"Number Completed: {completed}")
        print(f"Number In Progress: {in_progress}")
        print(f"Number Scheduled: {scheduled}")
