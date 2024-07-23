# Waveshare 0.96inch OLED Module via SPI (SSD1315)
# Available in White, Blue or Yellow & Blue
# Tony Goodhew 2 June 2023 - for thepihut.com

# Connect Red to 3.3V and Black to GND
from machine import Pin, SPI
import ssd1306

# Uses SPI port 0
spi_port = 0
MOSI = 19     # blue
CLK = 18      # yellow
CS = 17       # orange
RST = 16      # white   #NB MISO not used
DC = 20       # green

WIDTH = 128
HEIGHT = 64

spi = SPI(
    spi_port,
    baudrate=40000000,
    mosi=Pin(MOSI),
    sck=Pin(CLK))
print(spi) # Not essential - comment out

oled = ssd1306.SSD1306_SPI(WIDTH,HEIGHT,
    spi,
    dc=Pin(DC),
    res=Pin(RST),
    cs=Pin(CS),
    external_vcc=False
    )

# Clear the oled display in case it has junk on it.
oled.fill(0)

# Add some text
oled.text("Pi Pico with", 5, 6, 1)
oled.text('WS 0.96" OLED', 5, 16, 1)
oled.text("SSD1315 SPI", 5, 25, 1)
oled.text('White, Blue or', 5, 36, 1)
oled.text('Yellow & Blue', 5, 46, 1)
oled.text("thepihut.com", 5, 57, 1)

# Finally update the oled display so the text is displayed
oled.show()
