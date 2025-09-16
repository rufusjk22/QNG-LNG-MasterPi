from gpiozero import Servo

import time

# Use PiGPIO factory for better PWM precision

# Servo config (assuming PCA9685 on address 0x40, default)
from adafruit_pca9685 import PCA9685
from board import SCL, SDA
import busio

# Setup I2C
i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c)
pca.frequency = 50  # Standard for servos

# Helper: create servo using gpiozero with PCA9685 channel
def create_servo(channel):
    return Servo(channel,
                 min_pulse_width=0.5/1000,   # 0.5ms
                 max_pulse_width=2.5/1000,   # 2.5ms
                )

# Assign servos
claw     = create_servo(0)
joint1   = create_servo(1)
joint2   = create_servo(2)
joint3   = create_servo(3)
base     = create_servo(4  )

# Example: move joints
print("Moving arm...")
base.mid()     # neutral
joint1.min()   # move joint 1 fully
time.sleep(1)
joint1.max()
time.sleep(1)

claw.min()     # close claw
time.sleep(1)
claw.max()     # open claw
