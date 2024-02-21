import os
import glob
import argparse
import subprocess
from pathlib import Path

parser = argparse.ArgumentParser(
	prog='v2s',
	description='Converts a video into multiple spritesheets, and uploads them all to Roblox.'
)

parser.add_argument('-f', '--fps', default=10)
parser.add_argument('-i', '--input', required=True)
parser.add_argument('-w', '--width', required=True)
parser.add_argument('-s', '--seg_time', required=True)

args = parser.parse_args()
video = Path(args.input)

if not video.exists():
	print("v2s: error: %s doesn't exist" % args.input)
	raise SystemExit(1)

try:
	fps = int(args.fps)
except ValueError:
	print("v2s: error: fps must be an integer")
	raise SystemExit(1)

try:
	width = int(args.width)
except ValueError:
	print("v2s: error: width must be an integer")
	raise SystemExit(1)

try:
	time = int(args.seg_time)
except ValueError:
	print("v2s: error: seg_time must be an integer")
	raise SystemExit(1)

print("splitting %s into segments of %d seconds with an fps of %d and a width of %d" % (os.path.basename(args.input), time, fps, width))

base = 'out/%s' % video.stem

if not Path(base).exists():
	os.mkdir(base)

	if not Path(base + '/segs').exists():
		os.mkdir(base + '/segs')

subprocess.run(
	'ffmpeg -i %s -an -reset_timestamps 1 -force_key_frames "expr:gte(t,n_forced*%d)" -r %d -filter:v fps=%d -filter:v scale=%d:-2 -map 0 -segment_time %d -f segment "out/%s/segs/%%d.mp4"' %
	(args.input, time, fps, fps, width, time, video.stem),
	shell=True
)

if not Path(base + '/frames').exists():
	os.mkdir(base + '/frames')

if not Path(base + '/sheets').exists():
	os.mkdir(base + '/sheets')

os.system("python spriter.py " + video.stem)
