from flask import render_template, send_file, request, redirect
from scribe import app,datadir,modeldir
from scribe.transcriber import run_transcriber

import os,json
import shutil

#modeldir='/home/brenda/dev/kaldi/models'

def readinfo(infofile, id=None) :
    f = open (infofile)
    tr = {}
    tr['id']=id
    for l in f :
       x = l.strip().split('=')
       if (len(x) == 2) :
          tr[x[0]] = x[1]
    f.close()
    return tr


@app.route('/')
@app.route('/index')
def index() :
   return render_template('index.html',
                           user='Brenda')


@app.route('/files')
def fileList() :
   transcripts = []
   dirs = os.listdir(datadir)
   print(datadir, dirs)
   for dir in dirs :
        if os.path.exists(datadir + '/' + dir + '/.info') :
            infofile = datadir + '/' + dir + "/.info"
            tr = readinfo(infofile, id=dir)
            if 'status' not in tr :
                tr['status'] = 'Unknown'
            if 'status' in tr and 'text' in tr :
                transcripts.append(tr)
   print(transcripts)
   return render_template('files.html',
                           user='Brenda',
                           content=datadir,
                           transcripts=transcripts)




@app.route('/<trid>.html')
def default_template(trid) :
    return render_template(trid + ".html")

@app.route('/transcript/<trid>')
def transcript(trid) :
    if not os.path.exists(datadir + '/' + trid) : 
        return "dir not found"
    if not os.path.exists(datadir + '/' + trid + "/transcript.txt") : 
        return "file not found"
    tr = readinfo(datadir + '/' + trid + "/.info")
    trans = datadir + '/' + trid + "/transcript.txt"
    print('Returning ' + trans)
    textonly = request.args.get('textonly')
    if textonly is not None :
        return send_file(trans)
    t = open(trans, 'r')
    trdata = []
    for l in t :
       x = l.strip().split(' ', 1)
       if (len(x) != 2) :
           continue
       (pref, frame) = x[0].split('_')
       secs = int(frame) / 100.0
       mins = int (secs / 60)
       secs -= mins * 60.0 
       msecs = secs - int(secs)
       trdata.append(("%4d:%02d.%01d" % (mins,secs,int(msecs*10)), x[1], trid, frame))
       
    return render_template('transcript.html', transcript=trans, 
                             label=tr['text'], data=trdata, user='Brenda')

   
@app.route('/audio/<trid>')
def audio(trid) :
    if not os.path.exists(datadir + '/' + trid) : 
        return "dir not found"
    if not os.path.exists(datadir + '/' + trid + "/audio8k.wav") : 
        return "file not found"
    wav = datadir + '/' + trid + "/audio8k.wav"
    start = request.args.get('start')
    if start is not None :
       wav = datadir + "/" + trid + "/audio8k-" + start + ".wav"

    return send_file(wav)

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
    print("Saving file to " + newfile)
    
    file.save(newfile) 
    run_transcriber(workdir, modeldir)
    return redirect('/')
    #return file.filename

@app.route('/favicon.ico')
def icon() :
  return app.send_static_file('favicon.ico')

import sys

@app.route('/delete-transcript/<trid>', methods=['POST'])
def delete_transcript(trid) :
    print("DELETE " + trid)
    if os.path.exists(datadir + '/' + trid + '/.info') :
        tr = readinfo(datadir + "/" + trid + "/.info", id=dir)
        if tr['status'] != "Complete" :
            # stop
            print("Stopping job : " + trid)

        if not os.path.isdir(datadir + "/.trash") :
            os.makedirs(datadir + "/.trash")
            
        shutil.move(datadir + "/" + trid, datadir + "/.trash")
        #sys.stderr.write('shutil.move(datadir + "/" + trid, datadir + "/.trash")\n')
        
        return "Delete OK"
    else :
        return "Not found"
