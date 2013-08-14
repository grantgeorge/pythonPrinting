#!/usr/bin/python

# python imports
import sys

# library imports
import win32print
import win32ui
from PIL import Image, ImageWin

print("---ARGS---")
print sys.argv[1]

#
# Constants for GetDeviceCaps
#

#
# HORZRES / VERTRES = printable area
#

#
# DEFAULTS
#HORZRES = 8
#VERTRES = 10
#

HORZRES = 8
VERTRES = 10

#
# LOGPIXELS = dots per inch
#
LOGPIXELSX = 300
LOGPIXELSY = 600


#
# PHYSICALWIDTH/HEIGHT = total area
#

#
# DEFAULTS
# PHYSICALWIDTH = 110
# PHYSICALHEIGHT = 111
#

PHYSICALWIDTH = 110
PHYSICALHEIGHT = 111

#
# PHYSICALOFFSETX/Y = left / top margin
#

#
# DEFAULTS
#
#PHYSICALOFFSETX = 112
#PHYSICALOFFSETY = 113

PHYSICALOFFSETX = 112
PHYSICALOFFSETY = 113

# List available printers
print("Available printers")
#print(win32print.EnumPrinters(0,"None",1))
#print(win32print.EnumPrinters(1,"None",2))
print(win32print.EnumPrinters(3,"None",1)[4])
#print(win32print.EnumPrinters(3,"None",5))

# Use Default Printer
printer_name = win32print.GetDefaultPrinter ()
print("Printer: " + printer_name)

# Or explicitly define printer by name
#printer_name = "QL-710W"
file_name = sys.argv[1]

#
# You can only write a Device-independent bitmap
#  directly to a Windows device context; therefore
#  we need (for ease) to use the Python Imaging
#  Library to manipulate the image.
#
# Create a device context from a named printer
#  and assess the printable size of the paper.
#
hDC = win32ui.CreateDC ()
hDC.CreatePrinterDC (printer_name)
printable_area = hDC.GetDeviceCaps (HORZRES), hDC.GetDeviceCaps (VERTRES)

print("printable_area")
print(printable_area)

printer_size = hDC.GetDeviceCaps (PHYSICALWIDTH), hDC.GetDeviceCaps (PHYSICALHEIGHT)

print("printer_size")
print(printer_size)

printer_margins = hDC.GetDeviceCaps (PHYSICALOFFSETX), hDC.GetDeviceCaps (PHYSICALOFFSETY)

print("printer_margins")
print(printer_margins)

#
# Open the image, rotate it if it's wider than
#  it is high, and work out how much to multiply
#  each pixel by to get it as big as possible on
#  the page without distorting.
#
bmp = Image.open (file_name)

print("bmp.size[0]")
print(bmp.size[0])

print("bmp.size[1]")
print(bmp.size[1])

if bmp.size[0] > bmp.size[1]:
  bmp = bmp.rotate (90)

ratios = [1.0 * printable_area[0] / bmp.size[0], 1.0 * printable_area[1] / bmp.size[1]]

print("ratios")
print(ratios)

scale = min (ratios)

print("scale")
print(scale)

#
# Start the print job, and draw the bitmap to
#  the printer device at the scaled size.
#

hDC.StartDoc (file_name)
hDC.StartPage () 

dib = ImageWin.Dib (bmp)
scaled_width, scaled_height = [int (scale * i) for i in bmp.size]

print("scaled width")
print(scaled_width)

print("scaled height")
print(scaled_height)



x1 = int ((printer_size[0] - scaled_width) / 2)
y1 = int ((printer_size[1] - scaled_height) / 2)
x2 = x1 + scaled_width
y2 = y1 + scaled_height

print("x1, y1, x2, y2")
print(x1, y1, x2, y2)

# Default
dib.draw (hDC.GetHandleOutput (), (x1, y1, x2, y2))

# Custom
#dib.draw (hDC.GetHandleOutput (), (150, 150, 449, 688))

hDC.EndPage ()
hDC.EndDoc ()
hDC.DeleteDC ()