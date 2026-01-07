import bcrypt
from db import get_db

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def verify(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)

def login(email, password):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM users WHERE email=? AND is_active=1", (email,))
    user = cur.fetchone()
    if user and verify(password, user["password"]):
        return user
    return None
