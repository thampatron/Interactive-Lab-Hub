import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
from time import strftime, sleep

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

def showBaby():

	# Make sure to create image with mode 'RGB' for full color.
	if disp.rotation % 180 == 90:
    		height = disp.width  # we swap height/width to rotate it to landscape!
    		width = disp.height
	else:
    		width = disp.width  # we swap height/width to rotate it to landscape!
    		height = disp.height
	image = Image.new("RGB", (width, height))

# Get drawing object to draw on image.
	draw = ImageDraw.Draw(image)
  # Draw a black filled box to clear the image.
	draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
	disp.image(image)

	image = Image.open("/home/pi/Interactive-Lab-Hub/baby-photo.jpg")
	backlight = digitalio.DigitalInOut(board.D22)
	backlight.switch_to_output()
	backlight.value = True


	# Scale the image to the smaller screen dimension
	image_ratio = image.width / image.height
	screen_ratio = width / height
	if screen_ratio < image_ratio:
	    scaled_width = image.width * height // image.height
	    scaled_height = height
	else:
	    scaled_width = width
	    scaled_height = image.height * width // image.width
	image = image.resize((scaled_width, scaled_height), Image.BICUBIC)

	# Crop and center the image
	x = scaled_width // 2 - width // 2
	y = scaled_height // 2 - height // 2
	image = image.crop((x, y, x + width, y + height))
	disp.image(image)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True
count = 0

while True:
    # Draw a black filled box to clear the image.
    if count % 8 == 0:
        showBaby()
    else:
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        
        sec = int(strftime("%S"))
        min = int(strftime("%M"))
        hou = int(strftime("%H"))
        babies = int((sec + min*60 + hou*60*60)/8)

        text = "Babies born today: " + str(babies)
        draw.text((x,top), text, font=font)
        text = "New baby in " + str((8-count%8)) + "..."
        draw.text((x,font.getsize(text)[1]), text, font=font)


        w = (width/8)*(count%8)
        draw.rectangle((0,2*font.getsize(text)[1],w,height), outline=0,fill="#e5eb34")


    #TODO: fill in here. You should be able to look in cli_clock.py and stats.py 
        
# Display image
        disp.image(image, rotation)
    	
    time.sleep(1)
    count+=1