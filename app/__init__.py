from flask import Flask

webapp = Flask(__name__)

# from app import classify
from app import router
