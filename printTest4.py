#!/usr/bin/python

# python imports
# import platform
import sys

# library imports
import win32ui
import win32print
import win32gui
import win32con

from PIL import Image, ImageWin

def main(*args):
    # check platform
    # platform is stored in string platform
    # platform = platform.system()
    # if(platform == 'Windows'):
    #   print("OS: Windows")
    # elif(platform == 'Linux'):
    #   print("OS: Linux")
    # else:
    #   print("OS: iOS")

    num_args = len(sys.argv)

    print("Num textblocks: ", ((num_args -7) /5))

    if num_args == 7:
        print("No textblocks")
    elif (num_args -7 ) % 5 == 0:
        print("Ok")
    else:
        print("Not a valid input")

    def make_textblock(text, posx, posy, style, size):
        textblock = TextBlock(text, posx, posy, style, size)
        return textblock

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

    font_family = sys.argv[1]

    img_posx    = int(sys.argv[2])
    img_posy    = int(sys.argv[3])
    img_path    = sys.argv[4]
    img_height  = int(sys.argv[5])
    img_width   = int(sys.argv[6])

    text_blocks = []

    arg_inc = 7

    if (num_args == 7):
        print("No textblocks")
    else:
        while(arg_inc<num_args):
            text_blocks.append(make_textblock(sys.argv[arg_inc], sys.argv[arg_inc+1], sys.argv[arg_inc+2], sys.argv[arg_inc+3], sys.argv[arg_inc+4]))
            arg_inc = arg_inc + 5

    print("Font family: "  + font_family)

    print("img_posx: "      , img_posx)
    print("img_posy: "      , img_posy)
    print("img_path: "      + img_path)
    print("img_height: "    , img_height)
    print("img_width: "     , img_width)

    for text_block in text_blocks:
        print("Field " + text_block.text + "'s text: " + text_block.text)
        print("Field " + text_block.text + "'s posx: ", text_block.posx)
        print("Field " + text_block.text + "'s posy: ", text_block.posy)
        print("Field " + text_block.text + "'s font style: " + text_block.font_style)
        print("Field " + text_block.text + "'s font size: ", text_block.font_size)

    # if you just want to use the default printer, you need
    # to retrieve its name.
    printer = win32print.GetDefaultPrinter()
    print("Printer: " + printer)

    # open the printer.
    hprinter = win32print.OpenPrinter(printer)

    # retrieve default settings.  this code does not work on
    # win95/98, as GetPrinter does not accept two 
    devmode = win32print.GetPrinter(hprinter, 2)["pDevMode"]

    #
    # Taken from print_desktop.py
    # Not sure what it does
    #

    # dmsize=win32print.DocumentProperties(0, hprinter, printer, None, None, 0)
    # ## dmDriverExtra should be total size - fixed size
    # driverextra=dmsize - pywintypes.DEVMODEType().Size  ## need a better way to get DEVMODE.dmSize
    # dm=pywintypes.DEVMODEType(driverextra)
    # dm.Fields=dm.Fields|win32con.DM_ORIENTATION|win32con.DM_COPIES
    # dm.Orientation=win32con.DMORIENT_LANDSCAPE
    # dm.Copies=2
    # win32print.DocumentProperties(0, hprinter, printer, dm, dm, win32con.DM_IN_BUFFER|win32con.DM_OUT_BUFFER)

    # change paper size and orientation
    # constants are available here:
    # http://msdn.microsoft.com/library/default.asp?
    #      url=/library/en-us/intl/nls_Paper_Sizes.asp
    # number 10 envelope is 20

    # This doesn't do anything upon inspection
    # devmode.PaperSize = 333
    # devmode.Orientation = 2

    # create dc using new settings.
    # first get the integer hDC value.  note that we need the name.
    hdc = win32gui.CreateDC("WINSPOOL", printer, devmode)

    printerwidth=win32print.GetDeviceCaps(hdc, win32con.PHYSICALWIDTH)
    printerheight=win32print.GetDeviceCaps(hdc, win32con.PHYSICALHEIGHT)

    # next create a PyCDC from the hDC.
    dc = win32ui.CreateDCFromHandle(hdc)

    print("Printer length x width:")
    print(printerwidth)
    print(printerheight)

    # now you can set the map mode, etc. and actually print.

    # you need to set the map mode mainly so you know how
    # to scale your output.  I do everything in points, so setting 
    # the map mode as "twips" works for me.
    dc.SetMapMode(win32con.MM_TWIPS) # 1440 per inch

    # here's that scaling I mentioned:
    scale_factor = 20 # i.e. 20 twips to the point

    # Variables
    # font_size = 30

    bmp = Image.open (img_path)

    print("bmp.size[0]")
    print(bmp.size[0])

    print("bmp.size[1]")
    print(bmp.size[1])

    # if bmp.size[0] > bmp.size[1]:
    # bmp = bmp.rotate (90)

    # font = win32ui.CreateFont({
    #     "name": font_family,
    #     "height": int(scale_factor * font_size),
    #     "weight": 1,
    # })

    # 1 inch = scale_factor * 72
    # 1 inch = 1440 twips

    # start the document.  the description variable is a string
    # which will appear in the print queue to identify the job.
    dc.StartDoc("Nametag printjob")

    dib = ImageWin.Dib (bmp)

    #
    # SAMPLE, EXPLICIT COORDINATE DRAW
    # 2.40" x 3.90" with 0.12" FEED
    #

    # dib.draw (dc.GetHandleOutput (), (
    #     int(1.39 * scale_factor * 72),
    #     int(.2 * scale_factor * -72),
    #     int(2.39 * scale_factor * 72),
    #     int(1.2 * scale_factor * -72)
    #     ))

    # dc.TextOut(int(.89 * scale_factor * 72), int(1.3 * scale_factor * -72), "Grant")

    # dc.TextOut(int(1.89 * scale_factor * 72), int(1.3 * scale_factor * -72), "George")

    # dc.SelectObject(font_small)

    # dc.TextOut(int(1.49 * scale_factor * 72), int(1.8 * scale_factor * -72), "Title")

    # END SAMPLE

    dib.draw (dc.GetHandleOutput (), (
        img_posx,
        img_posy * -1,
        img_posx + img_width,
        (img_posy + img_height) * -1
        ))


    # to draw anything (other than text) you need a pen.
    # the variables are pen style, pen width and pen color.
    pen = win32ui.CreatePen(0, int(scale_factor), 0L)

    # SelectObject is used to apply a pen or font object to a dc.
    dc.SelectObject(pen)

    # again with the SelectObject call.
    # dc.SelectObject(font)

    for text_block in text_blocks:
        font = win32ui.CreateFont({
            "name": font_family,
            "height": scale_factor * text_block.font_size,
            "weight": 1
        })
        dc.SelectObject(font)
        print (text_block.text)
        print (text_block.posx)
        print (text_block.posy)
        dc.TextOut(text_block.posx, text_block.posy * -1, text_block.text)

    # Half Vertical Line
    # dc.MoveTo((int(1.89 * scale_factor * 72), int(0 *scale_factor * -72)))
    # dc.LineTo((int(1.89 * scale_factor * 72), int(2.4 * scale_factor* -72)))

    # # Half Horizontal Line
    # dc.MoveTo((int(0 * scale_factor * 72), int(1.2 *scale_factor * -72)))
    # dc.LineTo((int(3.78 * scale_factor * 72), int(1.2 * scale_factor* -72)))

    # # 1/3 Horizontal Line
    # dc.MoveTo((int(0 * scale_factor * 72), int(.8 *scale_factor * -72)))
    # dc.LineTo((int(3.78 * scale_factor * 72), int(.8 * scale_factor* -72)))

    # # 2/3 Horizontal Line
    # dc.MoveTo((int(0 * scale_factor * 72), int(1.6 *scale_factor * -72)))
    # dc.LineTo((int(3.78 * scale_factor * 72), int(1.6 * scale_factor* -72)))

    # must not forget to tell Windows we're done.
    dc.EndDoc()
    dc.DeleteDC()

if __name__ == "__main__":
    main(sys.argv[1:])