#!/usr/bin/python

# python imports
import platform
import sys

# imports
from PIL import Image, ImageFont, ImageDraw

def get_platform():
	return platform.system()

def check_version():
	if not sys.version_info[:2] == (2, 7):
		return False
	else:
		return True

def open_image():
	box = (0, 0, 120, 120)
	im = Image.open('./logo.png')
	region = im.crop(box)
	im.show()
	new_im = Image.new("RGB", (360, 250), "white")
	new_im.paste(region, (120,20,240,140))

	font = ImageFont.truetype('/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-B.ttf',35)
	font_small = ImageFont.truetype('/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-B.ttf',30)
	draw = ImageDraw.Draw(new_im)
	draw.text((100, 150),"Marina Lamb",(0,0,0),font=font)
	draw.text((140, 180),"Alumni",(0,0,0),font=font_small)
	draw = ImageDraw.Draw(new_im)
	draw = ImageDraw.Draw(new_im)
	new_im.save("a_test.png")
	new_im.show()
new
	new_im.save('new.png')

def print_linux():
	print ("You've reached the print_linux function")

	open_image()
	return

def print_mac():
	return

def print_windows():
	return

def main():
	system_platform = get_platform()
	if(check_version):
		print("Correct python version")
	else:
		print("Incorrect python")

	if(system_platform) == "Mac":
		print_mac()
	elif(system_platform) == "Windows":
		print_windows()
	else:
		print_linux()

if __name__ == '__main__':
	main()