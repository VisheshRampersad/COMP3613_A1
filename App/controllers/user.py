from App.models import User
from App.database import db

def create_user(username, password, email, role='staff'):

    user = User(username=username, password=password, email=email, role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    print(f"User {username} created!")
    
def login(username, password):
    user = User.query.filter_by(username=username).first()
    
    if user and user.check_password(password):
        print(f"Login successful!")
    else:
        print("Login failed!")


def get_user_by_username(username):
    result = db.session.execute(db.select(User).filter_by(username=username))
    return result.scalar_one_or_none()

def get_user(id):
    return db.session.get(User, id)

def get_all_users():

    users = User.query.all()
    
    print(f"Users ({len(users)} total)")

    for user in users:
        print(f"ID: {user.id}: {user.username} - {user.email} - ({user.role})")

def get_user_by_role(role):
    return db.session.scalars(db.select(User).filter_by(role=role)).all()

def get_all_users_json():
    users = get_all_users()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users


#for testing part in test_app.py
def update_user(id, username, email=None, role=None):
    user = get_user(id)
    if user:
        if username: user.username = username
        if email: user.email = email
        if role: user.role = role
        db.session.commit()
        return user
    return None
