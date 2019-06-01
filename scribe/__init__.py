from flask import Flask
from os.path import expanduser
home = expanduser("~")

datadir=home + '/.scribedata/'
modeldir="/opt/software/kaldi/models/aspire"

app = Flask(__name__)
from scribe import views

