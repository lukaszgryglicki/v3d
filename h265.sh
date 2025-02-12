#!/bin/bash
# VLIB=libx265
# CRF=27
# PRESET=slow
# ALIB=aac
# ABR=96k
# EXT=mp4
# SCALE=1280
if [ -z "$1" ]
then
  echo "$0: you need to specify the input file name"
  exit 1
fi
if [ -z "$VLIB" ]
then
  # export VLIB=libx264
  export VLIB=libx265
fi
if [ -z "$CRF" ]
then
  # from 0 to 51, sane ranges: 17-28
  # for h264 default is 23
  # for x265 default is 28
  export CRF=27
fi
if [ -z "$PRESET" ]
then
  # ultrafast superfast veryfast faster fast medium slow slower veryslow placebo
  export PRESET=slow
fi
if [ -z "$ALIB" ]
then
  # copy
  export ALIB=aac
fi
if [ -z "$ABR" ]
then
  export ABR=96k
fi
if [ -z "$EXT" ]
then
  export EXT=mp4
fi
if [ -z "$SCALE" ]
then
  echo "ffmpeg -threads 8 -re -i \"$1\" -c:v \"$VLIB\" -crf \"$CRF\" -preset \"$PRESET\" -c:a \"$ALIB\" -b:a \"$ABR\" \"$1.$EXT\""
  ffmpeg -threads 8 -re -i "$1" -c:v "$VLIB" -crf "$CRF" -preset "$PRESET" -c:a "$ALIB" -b:a "$ABR" "$1.$EXT"
  echo "ffmpeg -threads 8 -re -i \"$1\" -c:v \"$VLIB\" -crf \"$CRF\" -preset \"$PRESET\" -c:a \"$ALIB\" -b:a \"$ABR\" \"$1.$EXT\""
else
  echo "ffmpeg -threads 8 -re -i \"$1\" -filter:v \"scale=$SCALE:-2\" -c:v \"$VLIB\" -crf \"$CRF\" -preset \"$PRESET\" -c:a \"$ALIB\" -b:a \"$ABR\" \"$1.$EXT\""
  ffmpeg -threads 8 -re -i "$1" -filter:v "scale=$SCALE:-2" -c:v "$VLIB" -crf "$CRF" -preset "$PRESET" -c:a "$ALIB" -b:a "$ABR" "$1.$EXT"
  echo "ffmpeg -threads 8 -re -i \"$1\" -filter:v \"scale=$SCALE:-2\" -c:v \"$VLIB\" -crf \"$CRF\" -preset \"$PRESET\" -c:a \"$ALIB\" -b:a \"$ABR\" \"$1.$EXT\""
fi
