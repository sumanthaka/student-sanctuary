class Config:
    SECRET_KEY = 'random key'
    MONGODB_DATABASE_URI = "mongodb://localhost:27017"
    MYSQL_DATABASE_URI = "mysql+mysqlconnector://localhost:3307/student_sanctuary"
    MYSQL_DATABASE_HOST = "localhost"
    MYSQL_DATABASE_PORT = "3307"
    MYSQL_DATABASE_USER = "root"
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'email'
    MAIL_PASSWORD = 'password'