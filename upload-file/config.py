class Config:
    '''
    Stores the application's configuration settings
    '''

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://mark:7hhYhn>4@localhost/flaskpractice'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'mykey'
    UPLOAD_FOLDER = '~/Projects/flask/upload-file/static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
