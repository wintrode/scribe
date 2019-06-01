import sys
import os
import subprocess



def run_transcriber_serial(dirname, modeldir) :
    path = os.path.dirname(os.path.realpath(__file__))
    os.system('bash %s/../scripts/run_kaldi.sh %s %s > %s/.stdout 2> %s/.stderr' % (path, dirname, modeldir, dirname, dirname))

#def run_transcriber_thread(dirname) :
def run_transcriber(dirname, modeldir) :
    path = os.path.dirname(os.path.realpath(__file__))
    cmd = 'bash %s/../scripts/run_kaldi.sh %s %s > %s/.stdout 2> %s/.stderr' % (path, dirname, modeldir, dirname, dirname)
    subprocess.Popen(cmd, shell=True)
    # don't join - limit # of threads?
