from flask import Flask
from flask_triangle import Triangle

from os.path import expanduser
home = expanduser("~")

datadir=home + '/.scribedata/'
modeldir="/opt/software/kaldi/models/aspire"

app = Flask(__name__)
Triangle(app)

from scribe import views

