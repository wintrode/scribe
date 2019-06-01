#!flask
import scribe
import sys, os

if len(sys.argv) > 1 :
   scribe.datadir='.scribedata'

if not os.path.exists(scribe.datadir) :
   os.makedirs(scribe.datadir)

print("Writing to " + scribe.datadir)
   
scribe.app.run(debug=True)

