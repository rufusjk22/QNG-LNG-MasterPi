import smbus2
import time

# PCA9685 default address
ADDRESS = 0x40
bus = smbus2.SMBus(1)

# Registers
MODE1 = 0x00
PRESCALE = 0xFE
LED0_ON_L = 0x06

# Initialize PCA9685
bus.write_byte_data(ADDRESS, MODE1, 0x00)  # Normal mode

# Set frequency (50 Hz for servos)
freq = 50
prescale = int(25000000.0 / (4096 * freq) - 1)
oldmode = bus.read_byte_data(ADDRESS, MODE1)
bus.write_byte_data(ADDRESS, MODE1, (oldmode & 0x7F) | 0x10)  # sleep
bus.write_byte_data(ADDRESS, PRESCALE, prescale)
bus.write_byte_data(ADDRESS, MODE1, oldmode)
time.sleep(0.005)
bus.write_byte_data(ADDRESS, MODE1, oldmode | 0x80)

# Helper to set pulse
def set_servo(channel, on, off):
    reg = LED0_ON_L + 4 * channel
    bus.write_i2c_block_data(ADDRESS, reg, [on & 0xFF, on >> 8, off & 0xFF, off >> 8])

# Move servo on channel 0
while True:
    set_servo(0, 0, 150)   # one extreme
    time.sleep(1)
    set_servo(0, 0, 600)   # middle
    time.sleep(1)
    set_servo(0, 0, 1100)  # other extreme
    time.sleep(1)