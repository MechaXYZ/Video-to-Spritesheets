import re
import os
import cv2
import sys
import glob
import time
import requests
import rblxopencloud
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

id = os.getenv("V2S_UID")
key = os.getenv("V2S_KEY")

if not id:
	raise LookupError("V2S_UID was not set!")
elif not key:
	raise LookupError("V2S_KEY was not set!")

try:
	id = int(id)
except ValueError:
	raise ValueError("V2S_UID must be a number!")

user = rblxopencloud.User(id, api_key=key)

lua = '''local frames = {
'''

def process(id):
	try:
		result = requests.get("https://assetdelivery.roblox.com/v1/asset/?id=" + str(id)).text
		time.sleep(1)
		id = re.search('<url>(.*)</url', result).group(1)

		return id[32:]
	except (Exception, KeyboardInterrupt) as err:
		print("an error occured while getting image id, saving out.lua to " + os.getcwd())
		os.chdir('../../../')

		try:
			f = open('out.lua', 'w')
			f.write(lua)
			print('saved')
		except:
			print(lua)
		finally:
			os._exit(130)

		print("error: " + str(err))

def upload(path):
	file = open(path, "rb")

	try:
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
	except (Exception, KeyboardInterrupt) as err:
		print("an error occured while uploading, saving out.lua to " + os.getcwd())
		os.chdir('../../../')
		
		try:
			f = open('out.lua', 'w')
			f.write(lua)
			print('saved')
		except:
			print(lua)
		finally:
			os._exit(130)

		print("error: " + str(err))

def split(path):
	video = cv2.VideoCapture(path) 
	
	count = 0
	success = 1
	
	while success: 
		success, image = video.read()

		if success:
			cv2.imwrite('../frames/%d.png' % (count), image) 
	
			count += 1

def spriter(name):
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

	if master_width == 0:
		master_width = len(images) * image_width
	
	master_height += image_height

	master = Image.new(
		mode ='RGBA',
		size = (master_width, master_height),
		color = (0, 0, 0, 0)  # fully transparent
	)

	count = 0
	offset = 0

	for _, image in enumerate(images):
		if count * image_width > 1024:
			count = 0
			offset += image_height
		
		location = image_width * count
		master.paste(image, (location, offset))

		count += 1

	
	os.chdir('../')
	master.save('sheets/' + name)

	print('saved %s' % name)

	return master_width / image_width, master_height / image_height, len(images), name, master_width, master_height

def sheetify(vid):
	split(vid)

	os.chdir('../frames')
	cols, rows, frames, path, width, height = spriter(vid.split('.')[0] + '.png')

	os.chdir('./frames')
	leftovers = [fn for fn in glob.glob('*.png') if re.match(r'\d+.png', fn)]

	for f in leftovers:
		os.remove(f)
	
	os.chdir('../segs')
	return rows, cols, frames, path, width, height

os.chdir('out/' + sys.argv[1] + '/segs')

try:
	for i in range(len(glob.glob('*.mp4'))):
		rows, cols, frames, path, width, height = sheetify(str(i) + '.mp4')

		lua += '''    [%d] = {
			Rows = %d,
			Columns = %d,
			Frames = %d,
			Id = %s,
			ImageRectSize = Vector2.new(%d, %d)
		};
''' % (i, rows, cols, frames, upload('../sheets/' + path), width, height)

		print('uploaded %s' % path)

	lua += '}'

	os.chdir('../../../')

	try:
		print('saving to out.lua')
		f = open('out.lua', 'w')
		f.write(lua)
		print('saved')
	except:
		print(lua)
except (Exception, KeyboardInterrupt) as err:
	print("an error occured while uploading, saving out.lua to " + os.getcwd())
	os.chdir('../../../')
	
	try:
		f = open('out.lua', 'w')
		f.write(lua)
		f.close()
		print('saved')
	except:
		print(lua)
	finally:
		os._exit(130)

	print("error: " + str(err))