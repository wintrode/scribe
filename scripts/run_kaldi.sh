#!/bin/bash

# set KALDI_HOME
KALDI_HOME=$HOME/dev/kaldi

bindir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

workdir=$1
modeldir=$2

cd $workdir



if [ -f audio.wav ]; then
  audio=audio.wav
elif  [ -f audio.mp3 ]; then
  audio=audio.mp3
elif [ -f audio.m4a ]; then
  audio=audio.m4a
else
  echo "audio.[wav,mp3,m4a] not found"
  exit 1
fi

if [ ! -f audio8k.wav ]; then
ffmpeg -i $audio -acodec pcm_s16le -ac 1 -ar 8000 audio8k.wav
fi


ln -s $modeldir/exp exp
ln -s $modeldir/utils utils
cp $modeldir/path.sh .
#cp $modeldir/cmd.sh .

sed -i 's/^status=.*/status=In process/' .info

source path.sh

# run VAD
# create wav.scp, segments, spk2utt
echo testaudio audio8k.wav > wav.scp
# segments is seg_id testaudio start stop
# spk2utt is testaudio seg_id1 segid_2 ...
mkdir -p mfcc

if [ ! -f mfcc/raw_mfcc.ark ]; then
compute-mfcc-feats  --verbose=2 --config=$modeldir/mfcc.conf \
     scp,p:wav.scp ark:- | \
      copy-feats --write-num-frames=ark,t:utt2num_frames --compress=true ark:- \
      ark,scp:mfcc/raw_mfcc.ark,mfcc/raw_mfcc.scp
fi

if [ ! -f segments ]; then

compute-vad --config=$modeldir/vad.conf scp:mfcc/raw_mfcc.scp ark,scp:mfcc/vad.ark,mfcc/vad.scp
copy-vector ark:mfcc/vad.ark ark,t:- | sed 's/ /\n/g' | \
    perl $modeldir/vad_segment.pl testaudio
fi

# decode
source path.sh

online2-wav-nnet3-latgen-faster \
  --online=false \
  --do-endpointing=false \
  --frame-subsampling-factor=3 \
  --config=exp/tdnn_7b_chain_online/conf/online.conf \
  --max-active=7000 \
  --beam=15.0 \
  --lattice-beam=6.0 \
  --acoustic-scale=1.0 \
  --word-symbol-table=exp/tdnn_7b_chain_online/graph_pp/words.txt \
  exp/tdnn_7b_chain_online/final.mdl \
  exp/tdnn_7b_chain_online/graph_pp/HCLG.fst \
  'ark:spk2utt' \
  'ark,s,cs:extract-segments scp,p:wav.scp segments ark:- |' \
  'ark:|lattice-scale --acoustic-scale=10.0 ark:- ark:- | gzip -c > lat.1.gz'

lattice-scale --inv-acoustic-scale=10 "ark:gunzip -c lat.1.gz|" ark:- | \
      lattice-add-penalty --word-ins-penalty=0.5 ark:- ark:- | \
      lattice-prune --beam=6.0 ark:- ark:- | \
      lattice-align-words exp/tdnn_7b_chain_online/graph_pp/phones/word_boundary.int exp/tdnn_7b_chain_online/final.mdl ark:- ark:- | \
      lattice-to-ctm-conf --decode-mbr=true ark:- - | \
      utils/int2sym.pl -f 5  exp/tdnn_7b_chain_online/graph_pp/words.txt | \
      tee lat.1.ctm


perl $bindir/ctm2trans.pl lat.1.ctm > transcript.txt

sed -i 's/^status=.*/status=Complete/' .info

perl $bindir/split_wav.pl audio8k.wav segments
