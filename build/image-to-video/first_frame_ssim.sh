#!/bin/sh
# usage: first_frame_ssim.sh <video.mp4> <photo.jpg>  -> prints SSIM "All" score (0..1)
# Both sides are scaled to 360x640 grayscale so resolution and encoder chroma don't matter.
ffmpeg -nostdin -loglevel error -i "$1" -i "$2" -filter_complex \
  "[0:v]select=eq(n\,0),scale=360:640,format=gray[a];[1:v]scale=360:640,format=gray[b];[a][b]ssim=stats_file=-" \
  -frames:v 1 -f null - 2>/dev/null | sed -n 's/.*All:\([0-9.]*\).*/\1/p' | head -1
