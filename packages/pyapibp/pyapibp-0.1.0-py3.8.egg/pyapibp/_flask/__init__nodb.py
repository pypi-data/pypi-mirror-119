import os
from flask import Flask

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')

from app import routes
