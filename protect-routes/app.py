from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#initialize the flask app
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://mark:7hhYhn>4@localhost/flaskpractice'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)




if __name__ == '__main__':
    app.run(debug=True)
