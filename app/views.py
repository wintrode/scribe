from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index() :
   return render_template('index.html',
                           user='Brenda',
                           content='Upload your files here')

@app.route('/favicon.ico')
def icon() :
  return app.send_static_file('favicon.ico')
