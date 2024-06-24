"""
This module contains implementation of password hashing using Bcrypt
"""
from flask import Flask


app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)
