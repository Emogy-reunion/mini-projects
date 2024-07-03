from flask import Flask
from config import Config
from model import db, User
from form import RegistrationForm

#initialize the flask app
app = Flask(__name__)

#configure flask app with settings defined in the configuration file
app.config.from_object(Config)

#initialize the db instance with the app instance
db.init_app(app)



if __name__ == '__main__':
    app.run(debug=True)
