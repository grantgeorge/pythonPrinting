# python imports
import platform
import sys
import os

# imports
from PIL import Image, ImageFont, ImageDraw

def get_platform():
	return platform.system()

def check_version():
	if not sys.version_info[:2] == (2, 7):
		return False
	else:
		return True

def print_linux(font_family, img_posx, img_posy, img_path, img_height, img_width, text_blocks):
	print "made it to the print_linux function!"

	logo = Image.open(img_path)

	width, height = logo.size

	enlarged_logo = logo.resize((img_height, img_width), Image.ANTIALIAS)

	enlarged_logo.save('enlarged_logo', 'PNG')

	# Create blank image
	new_im = Image.new('RGB', (1800, 1000), 'white')

	# paste in enlarged logo
	new_im.paste(enlarged_logo, (img_posx, img_posy, img_posx + img_width, img_posy + img_height))

	draw = ImageDraw.Draw(new_im)

	for text_block in text_blocks:
		# Change to variable font
		font = ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf', text_block.font_size)
		draw.text((text_block.posx, text_block.posy), text_block.text, (0,0,0), font=font)

	# # some test lines
	# # horizontal line
	# draw.line((0,500,1800,500), fill=256)
	# draw.polygon([(0,500), (1800,500), (1800,525), (0,525)], fill='black', outline='black')

	# # vertical line
	# draw.line((900,0,900,1000), fill=256)
	# draw.polygon([(900,0), (900,1000), (925,1000), (925,0) ], fill='black', outline='black')

	new_im.show()

	new_im.save('nametag_print.png')

	# call lp to print
	# os.system(r'lp -d QL-700 ./nametag_print.png')

	return

def print_mac(font_family, img_posx, img_posy, img_path, img_height, img_width, text_blocks):
	return

def print_windows(font_family, img_posx, img_posy, img_path, img_height, img_width, text_blocks):
	return

def main():

	debug = 0

	system_platform = get_platform()
	if(check_version):
		print("Correct python version")
	else:
		print("Incorrect python")

	# Set variables

	num_args = len(sys.argv)

	# Validations
	if debug:
		print "Number of textblocks: ", ((num_args -7) /5)
		if num_args == 7:
			print("No textblocks")
		elif (num_args -7 ) % 5 == 0:
			print("System arguments valid")
		else:
			print("Not a valid input")

	font_family = sys.argv[1]

	img_posx    = int(sys.argv[2])
	img_posy    = int(sys.argv[3])
	img_path    = sys.argv[4]
	img_height  = int(sys.argv[5])
	img_width   = int(sys.argv[6])

	text_blocks = []

	# Incrementer used to track argument enumeration for textblock generation
	argument_incrementer = 7

	# If there are 7 arguments, no text blocks exist
	if num_args == 7:
		print("No textblocks")
	# Check that there are 5 arguments for each text block
	elif (num_args -7 ) % 5 != 0:
		print "System arguments invalid"
	# There are text blocks, create them
	else:
		while(argument_incrementer<num_args):
			text_blocks.append(make_textblock(sys.argv[argument_incrementer], sys.argv[argument_incrementer+1], sys.argv[argument_incrementer+2], sys.argv[argument_incrementer+3], sys.argv[argument_incrementer+4]))
			argument_incrementer = argument_incrementer + 5

	# Console print statments to check input
	if(debug):
		print "Font family: "  + font_family

		print "img_posx: "      , img_posx
		print "img_posy: "      , img_posy
		print "img_path: "      + img_path
		print "img_height: "    , img_height
		print "img_width: "     , img_width

		for text_block in text_blocks:
			print "Textblock " + text_block.text + "'s text: " + text_block.text
			print "Textblock " + text_block.text + "'s posx: ", text_block.posx
			print "Textblock " + text_block.text + "'s posy: ", text_block.posy
			print "Textblock " + text_block.text + "'s font style: " + text_block.font_style
			print "Textblock " + text_block.text + "'s font size: ", text_block.font_size

	print(system_platform)

	if(system_platform) == "Mac":
		print_linux(font_family, img_posx, img_posy, img_path, img_height, img_width, text_blocks)
	elif(system_platform) == "Windows":
		print_windows(font_family, img_posx, img_posy, img_path, img_height, img_width, text_blocks)
	else:
		print_linux(font_family, img_posx, img_posy, img_path, img_height, img_width, text_blocks)

class TextBlock(object):
	""" store text_field data """
	text        = ""
	posx        = 0
	posy        = 0
	font_style  = ""
	font_size   = 0

	def __init__(self, text, posx, posy, font_style, font_size):
		self.text       = text
		self.posx       = int(posx)
		self.posy       = int(posy)
		self.font_style = font_style
		self.font_size  = int(font_size)

def make_textblock(text, posx, posy, style, size):
	""" Function to create text blocks """
	textblock = TextBlock(text, posx, posy, style, size)
	return textblock

if __name__ == "__main__":
	main()