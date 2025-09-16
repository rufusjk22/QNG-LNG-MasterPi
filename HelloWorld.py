from gpiozero import DigitalOutputDevice, PWMOutputDevice,Servo
from time import sleep

LF_IN1, LF_IN2 = 17, 22
LB_IN1, LB_IN2 = 24, 25
RF_IN1, RF_IN2 = 5, 6
RB_IN1, RB_IN2 = 16, 26
PWM_PIN = 12
lf_in1 = DigitalOutputDevice(LF_IN1)
lf_in2 = DigitalOutputDevice(LF_IN2)
lb_in1 = DigitalOutputDevice(LB_IN1)
lb_in2 = DigitalOutputDevice(LB_IN2)
rf_in1 = DigitalOutputDevice(RF_IN1)
rf_in2 = DigitalOutputDevice(RF_IN2)
rb_in1 = DigitalOutputDevice(RB_IN1)
rb_in2 = DigitalOutputDevice(RB_IN2)
pwm = PWMOutputDevice(PWM_PIN, frequency=1000)
def set_motors(lf, lb, rf, rb, speed=0.5):
    lf_in1.value = 1 if lf == 1 else 0
    lf_in2.value = 1 if lf == -1 else 0
    lb_in1.value = 1 if lb == 1 else 0
    lb_in2.value = 1 if lb == -1 else 0
    rf_in1.value = 1 if rf == 1 else 0
    rf_in2.value = 1 if rf == -1 else 0
    rb_in1.value = 1 if rb == 1 else 0
    rb_in2.value = 1 if rb == -1 else 0
    pwm.value = speed if (lf or lb or rf or rb) else 0
def forward(speed=0.5):  set_motors(1, 1, 1, 1, speed)
def backward(speed=0.5): set_motors(-1, -1, -1, -1, speed)

def right(speed=0.5):    set_motors(1, -1, -1, 1, speed)
def left(speed=0.5):     set_motors(-1, 1, 1, -1, speed)

def rotate_cw(speed=0.5):  set_motors(1, 1, -1, -1, speed)
def rotate_ccw(speed=0.5): set_motors(-1, -1, 1, 1, speed)

def stop():
    set_motors(0, 0, 0, 0, 0)
    
#=====Diagonal Strafing======
def move_diag_left_forward(speed=50):
    LF_stop()
    RF_forward(speed)
    LB_forward(speed)
    RB_stop()

def move_diag_right_forward(speed=100):
    LF_forward(speed)
    RF_stop()
    LB_stop()
    RB_forward(speed)

def move_diag_left_backward(speed=100):
    LF_backward(speed)
    RF_stop()
    LB_stop()
    RB_backward(speed)

def move_diag_right_backward(speed=100):
    LF_stop()
    RF_backward(speed)
    LB_backward(speed)
    RB_stop()
try:
    forward(); sleep(2); stop()
    backward(); sleep(2); stop()
    left(); sleep(2); stop()
    right(); sleep(2); stop()
    rotate_cw(); sleep(2); stop()
    rotate_ccw(); sleep(2); stop()
finally:
    stop()
    pwm.close()
    lf_in1.close(); lf_in2.close()
    lb_in1.close(); lb_in2.close()
    rf_in1.close(); rf_in2.close()
    rb_in1.close(); rb_in2.close()