from flask import Flask
from os.path import expanduser
home = expanduser("~")

datadir=home + '/.scribedata/'

app = Flask(__name__)
from app import views

