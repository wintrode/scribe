#!/bin/bash

if [ -z $SCRIBE_ROOT ]; then
   SCRIBE_ROOT=/opt/software/scribe
fi


cmd=$1

if [ $cmd == "start" ]; then
  
  if [ -f $SCRIBE_ROOT/.scribe.pid ]; then
    echo "SCRIBE already  running"
    exit 1
  fi

  export FLASK_APP=scribe
  nohup flask run --host=0.0.0.0 &> $SCRIBE_ROOT/flask.log &
  echo $! > $SCRIBE_ROOT/.scribe.pid

elif [ $cmd == "stop" ]; then
  
  if [ -f $SCRIBE_ROOT/.scribe.pid ]; then
   pid=`cat $SCRIBE_ROOT/.scribe.pid`
   kill -9 $pid
   rm $SCRIBE_ROOT/.scribe.pid
  fi
fi

