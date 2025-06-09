# Configuration settings for the CV Analyzer application

class Config:
    DATABASE_URI = "mysql+pymysql://username:password@localhost:3306/cv_analyzer"
    SECRET_KEY = "your_secret_key"
    UPLOAD_FOLDER = "data/cv_samples"
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

    @staticmethod
    def is_allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS