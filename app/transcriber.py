from multiprocessing import Process
import sys
import os



def run_transcriber(dirname) :
    path = os.path.dirname(os.path.realpath(__file__))
    os.system('bash %s/../scripts/run_kaldi.sh %s > %s/.stdout 2> %s/.stderr' % (path, dirname, dirname, dirname))

def run_transcriber_thread(dirname) :
    p = Process(target=run_transcriber, args=(dirname,))
    p.start()
    # don't join - limit # of threads?
