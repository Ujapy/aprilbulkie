from project import db, login_manager, bcrypt, app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    #return User.query.get(int(user_id))
    return User.query.filter(User.id == int(user_id)).first()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username= db.Column(db.String(20), unique = True, nullable = False)
    firstname= db.Column(db.String(20), nullable = False)
    surname= db.Column(db.String(20), nullable = False)
    sex= db.Column(db.String(20), nullable = False)
    email= db.Column(db.String(120), unique = True, nullable = False)
    address= db.Column(db.String(300), nullable = False)
    phone= db.Column(db.Integer, unique = True, nullable = False)
    phone2= db.Column(db.Integer, unique = True)
    password= db.Column(db.String(60), nullable = False)
    authenticated = db.Column(db.Boolean, default=False)
    email_confirmation_sent_on = db.Column(db.DateTime, nullable=True)
    email_confirmed = db.Column(db.Boolean, nullable=True, default=False)
    email_confirmed_on = db.Column(db.DateTime, nullable=True)
    registered_on = db.Column(db.DateTime, nullable=True)
    last_logged_in = db.Column(db.DateTime, nullable=True)
    current_logged_in = db.Column(db.DateTime, nullable=True)


 
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')
    def __init__(self, username, firstname, surname, sex, email, address, phone, phone2, password, email_confirmation_sent_on=None):
        self.username = username
        self.firstname = firstname
        self.surname = surname
        self.sex = sex
        self.email = email
        self.address = address
        self.phone = phone
        self.phone2 = phone2
        self.password = password
        self.authenticated = False
        self.email_confirmation_sent_on = email_confirmation_sent_on
        self.email_confirmed = False
        self.email_confirmed_on = None
        self.registered_on = datetime.now()
        self.last_logged_in = None
        self.current_logged_in = datetime.now()
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return  f"User('{self.username}', '{self.firstname}', '{self.surname}','{self.sex}', '{self.email}', '{self.address}', '{self.phone}', '{self.phone2}')"
    
    def generate_auth_token(self, expires_in=3600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expires_in)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    def __repr__(self):
        return '<User {}>'.format(self.email)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_file = db.Column(db.String(20), nullable = False)
    description = db.Column(db.String(300), nullable = False)
    total_slot = db.Column(db.Integer, nullable = False)
    slot_value = db.Column(db.Integer, nullable = False)
    available_slot = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, nullable = False, default=datetime.utcnow)
    location = db.Column(db.String(500), nullable = False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)


    
    
    def __repr__(self):
        return  f"Post('{self.description}', '{self.total_slot}', '{self.slot_value}','{self.location}', '{self.image_file}', '{self.date_created}')"
