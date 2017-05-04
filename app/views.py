from flask import render_template, send_file, request, redirect
from app import app,datadir
from transcriber import run_transcriber

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
            if 'status' in tr and 'text' in tr :
                transcripts.append(tr)
   print(transcripts)
   return render_template('index.html',
                           user='Brenda',
                           content=datadir,
                           transcripts=transcripts)

                           
@app.route('/transcript/<trid>')
def transcript(trid) :
    if not os.path.exists(datadir + '/' + trid) : 
        return "dir not found"
    if not os.path.exists(datadir + '/' + trid + "/transcript.txt") : 
        return "file not found"
    
    trans = datadir + '/' + trid + "/transcript.txt"
    print('Returning ' + trans)
    return send_file(trans)
    
   
@app.route('/transcribe', methods=['POST'])
def transcribe() :
    print(request.method)
    if 'file' not in request.files :
         sys.stderr.write("No file attached\n")
         return redirect('/')

    file = request.files['file']
    # create tempdir
    # save file
    # spawn process
    transcripts = []
    dirs = os.listdir(datadir)
    label = request.form.get('label')
    print(label)
    if '/' in label :
       return 'Invalid label'

    label = label.replace(' ', '_')

    maxid=0
    for dir in dirs :
       id = int(dir)
       if (id > maxid) : maxid = id       

    id = maxid+1
       
    workdir = datadir + '/' + str(id)
    os.makedirs(workdir)
    f = open(workdir + '/.info', 'w')
    f.write('text=%s\n' % (label))
    f.write('status=Not started\n')
    f.close()
    g = file.filename.rsplit('.',1)
    if (len(g) != 2) : 
        return "Invalid file"
    ext = g[1]
    newfile = workdir + '/audio.' + ext
    print "Saving file to " + newfile
    
    file.save(newfile) 
    run_transcriber(workdir)
    return redirect('/')
    #return file.filename

@app.route('/favicon.ico')
def icon() :
  return app.send_static_file('favicon.ico')
