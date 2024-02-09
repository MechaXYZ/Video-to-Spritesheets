import re
import os
import sys
import glob
import time
import requests
import argparse
import rblxopencloud
from PIL import Image

id = 12345 # put your userid here
key = "foobar123" # put your api key here
user = rblxopencloud.User(id, api_key=key)

def process(id):
	result = requests.get("https://assetdelivery.roblox.com/v1/asset/?id=" + str(id)).text
	time.sleep(1)
	id = re.search('<url>(.*)</url', result).group(1)

	return id[32:]

def upload(path):
	file = open(path, "rb")

	asset = user.upload_asset(file, rblxopencloud.AssetType.Decal, "sprite", "Decal")
	time.sleep(1)

	if isinstance(asset, rblxopencloud.Asset):
		return process(asset.id)
	else:
		while True:
			time.sleep(1)
			operation = asset.fetch_operation()

			if operation:
				return process(operation.id)

def split(gif):
	frame = Image.open(gif)
	frameIdx = 0
	
	os.chdir('../frames')
	 
	try:
		while 1:
			frame.seek(frameIdx)
			frame.save('%s/%s.png' % (os.getcwd(), frameIdx),'png')
			frameIdx += 1
	except EOFError:
		pass

def spriter(mastername):
	if mastername is None:
		mastername = 'master.png'

	iconMap = [fn for fn in glob.glob('*.png') if re.match(r'\d+.png', fn)]
	iconMap = sorted(iconMap, key=lambda i: int(i.split('.')[0]))

	images = [Image.open(filename) for filename in iconMap]
	image_width, image_height = images[0].size

	count = 0
	master_width = 0
	master_height = 0

	for _ in enumerate(images):
		if count * image_width > 1024:
			rows = count
			master_width = image_width * count

			count = 0
			master_height += image_height

		count += 1

	master_height += image_height

	master = Image.new(
		mode ='RGBA',
		size = (master_width, master_height),
		color = (0, 0, 0, 0)  # fully transparent
	)

	count = 0
	offset = 0

	for c, image in enumerate(images):
		if count * image_width > 1024:
			count = 0
			offset += image_height
		
		location = image_width * count
		master.paste(image, (location, offset))

		count += 1

	
	os.chdir('../')
	master.save('sheets/' + mastername)

	print('saved %s' % mastername)

	return master_width / image_width, master_height / image_height, len(images), mastername

def gif_to_sprite(gif=None):
	split(gif)
	cols, rows, frames, path = spriter(gif.split('.')[0] + '.png')

	os.chdir('./frames')
	leftovers = [fn for fn in glob.glob('*.png') if re.match(r'\d+.png', fn)]

	for f in leftovers:
		os.remove(f)
	
	os.chdir('../gifs')

	return rows, cols, frames, path

os.chdir('out/' + sys.argv[1] + '/gifs')

lua = '''local frames = {
'''

for i in range(len(glob.glob('*.gif'))):
	rows, cols, frames, path = gif_to_sprite(str(i) + '.gif')

	lua += '''    [%d] = {
		["Rows"] = %d,
		["Columns"] = %d,
		["Frames"] = %d,
		["Id"] = %s
	};
''' % (i, rows, cols, frames, upload('../sheets/' + path))

	print('uploaded %s' % path)

lua += '}'

os.chdir('../../../')

try:
	print('saving to out.lua')
	f = open('out.lua', 'w+')
	f.write(lua)
	print('saved')
except:
	print(lua)