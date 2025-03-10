import os

class Config:
    # Cấu hình bảo mật
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'

    # Cấu hình cơ sở dữ liệu
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://admin:admin@localhost:3307/project_management'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Cấu hình thư mục tải lên
    UPLOAD_FOLDER = 'static/uploads'

    # Cấu hình email
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'your_email@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'your_password'

    # Cấu hình JWT
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # Token hết hạn sau 1 giờ
