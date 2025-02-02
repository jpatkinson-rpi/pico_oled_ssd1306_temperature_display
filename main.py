#-------------------------------------------------------------------
# RPi PICO temperature display
# - ssd1306 OLED (I2C) display
# - DS18x20 onewire temperature sensor on GPIO 22
#-------------------------------------------------------------------

from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import machine
import utime
import onewire, ds18x20, time
from writer import Writer
import freesans30 # Font
import icons # Font

ds_pin = machine.Pin(22)

ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))

roms = ds_sensor.scan()

print('Found DS devices: ', roms)

WIDTH  = 128                                            # oled display width
HEIGHT = 32                                             # oled display height

i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=200000)       # Init I2C using pins GP8 & GP9 (default I2C0 pins)
print("I2C Address      : "+hex(i2c.scan()[0]).upper()) # Display device address
print("I2C Configuration: "+str(i2c))                   # Display I2C config

oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)                  # Init oled display

while True:
 
   ds_sensor.convert_temp()

   time.sleep_ms(750)

   value = ds_sensor.read_temp(roms[0])
 
   # Clear the oled display in case it has junk on it.
   oled.fill(0)

   wri = Writer(oled, freesans30, verbose=False)
   value = ds_sensor.read_temp(roms[0])
   valuestr = '{:.1f}  C'.format(value)
   valuestr = '{:>4}'.format(valuestr)
   Writer.set_textpos(oled, 0, 20)
   wri.printstring(valuestr)
 
   wri = Writer(oled, icons, verbose=False)
   Writer.set_textpos(oled, 0, 78) # Position for degC symbol
   wri.printstring('F') # degC symbol
   oled.show()
   time.sleep(5)
