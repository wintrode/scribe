from flask import render_template, send_file, request
from app import app,datadir

import os,json

@app.route('/')
@app.route('/index')
def index() :
   transcripts = []
   dirs = os.listdir(datadir)
   print(datadir, dirs)
   for dir in dirs :
        print(dir)
        if os.path.exists(datadir + '/' + dir + '/.info') :
            f = open (datadir + '/' + dir + "/.info")
            tr = {}
            tr['id']=dir
            for l in f :
                x = l.strip().split('=')
                if (len(x) == 2) :
                    tr[x[0]] = x[1]
            f.close()
            if 'status' not in tr :
                tr['status'] = 'Unknown'
            if 'link' in tr and 'status' in tr and 'text' in tr :
                transcripts.append(tr)
   print(transcripts)
   return render_template('index.html',
                           user='Brenda',
                           content=datadir,
                           transcripts=transcripts)

                           
@app.route('/transcript/<trid>')
def transcript(trid) :
    if not os.path.exists(datadir + '/' + trid) : 
        return "not found"
    
    trans = datadir + '/' + trid + "/transcript.txt"
    print('Returning ' + trans)
    return send_file(trans)
    
   
@app.route('/transcribe', methods=['POST'])
def transcribe() :
    print(request.form)
    if 'file' not in request.files :
         return "No file attached"

    file = request.files['file']
    # create tempdir
    # save file
    # spawn process
    
    return file.filename

@app.route('/favicon.ico')
def icon() :
  return app.send_static_file('favicon.ico')
