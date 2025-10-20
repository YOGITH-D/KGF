from mining import db,bycrypt,login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id=db.Column(db.Integer(),primary_key=True)
    username=db.Column(db.String(length=30),nullable=False,unique=True)
    email_address=db.Column(db.String(length=50),nullable=False,unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute!')
    
    @password.setter
    def password(self,password_plain_text):
        self.password_hash=bycrypt.generate_password_hash(password_plain_text).decode('utf-8')

    
    def check_password_correction(self,attempted_password):
        return bycrypt.check_password_hash(self.password_hash,attempted_password)