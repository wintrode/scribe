#!flask/bin/python
import app
import sys, os

if len(sys.argv) > 1 :
   app.datadir='.scribedata'

if not os.path.exists(app.datadir) :
   os.makedirs(app.datadir)

print(app.datadir)
   
app.app.run(debug=True)

