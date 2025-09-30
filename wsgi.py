import click, pytest, sys
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User, Shift
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize )
from App.controllers.user import *
from App.controllers.shift import *
from App.controllers.roster import *

from datetime import datetime, date, timedelta

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    #sample data in initialize.py
    initialize()
    print('Database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# user commands

user_cli = AppGroup('user', help='User commands')

@user_cli.command("create", help="Create new user")
@click.argument("username")
@click.argument("password")
@click.argument("email")
@click.argument("role", default="staff")

def createuser(username, password, email, role):
    create_user(username=username, password=password, email=email, role=role)
    

@user_cli.command("list", help="List all users")
def list_users():
    get_all_users()

@user_cli.command("login", help="Test user login")

@click.argument("username")
@click.argument("password")
def test_login(username, password):
    login(username,password)

app.cli.add_command(user_cli)

#(Staff) View combined roster of all staff

roster_cli = AppGroup('roster', help='Roster commands')

@roster_cli.command("view", help="View combined roster")
@click.argument("start_date", required=False)
@click.argument("end_date", required=False)

def view_roster(start_date=None, end_date=None):
    get_roster(start_date, end_date)
   



#(Admin) Schedule a staff member shifts for the week
@roster_cli.command("schedule", help="Schedule shift")
@click.argument("admin_id")
@click.argument("user_id")
@click.argument("start_time")
@click.argument("end_time")
@click.argument("shift_date")

def schedule_shift(admin_id, user_id, start_time, end_time, shift_date):
    schedule(admin_id, user_id, start_time, end_time, shift_date)



@roster_cli.command("clock-in", help="Clock in for shift")
@click.argument("shift_id")
def clockin(shift_id):
    clock_in(shift_id)



@roster_cli.command("clock-out", help="Clock out shift")
@click.argument("shift_id")

def clockout(shift_id):
    clock_out(shift_id)


#(Admin) View shift report for the week
@roster_cli.command("report", help="View shift report")
@click.argument("user_id")
def shift_report(user_id):
    report(user_id)
   
app.cli.add_command(roster_cli)

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)