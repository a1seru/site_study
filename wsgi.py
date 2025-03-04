import os
from site_study1 import app

if __name__ != "__main__":
    app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')
    
