from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_moment import Moment
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap

#from project import app
app = Flask(__name__, instance_relative_config=True)


app.config.from_pyfile('flask.cfg')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)
moment = Moment(app)
login_manager = LoginManager()  
login_manager.init_app(app)
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"


mail = Mail(app)

from project.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()



from project.users.views import users_blueprint 
from project.admin import admin as admin_blueprint
app.register_blueprint(admin_blueprint, url_prefix='/admin')

from project.auth import auth as auth_blueprint

app.register_blueprint(auth_blueprint)
from project.users import views
# register the blueprints
app.register_blueprint(users_blueprint)


