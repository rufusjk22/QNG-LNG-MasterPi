import asyncio
import websockets
import subprocess
import os
from gpiozero import DigitalOutputDevice, PWMOutputDevice,Servo
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

# Start MJPG Streamer in the background
mjpg_path = os.path.expanduser("~/mjpg-streamer/mjpg-streamer-experimental/mjpg_streamer")
mjpg_process = subprocess.Popen([
    mjpg_path,
    "-i", "input_uvc.so -d /dev/video0 -r 640x480 -f 30",
    "-o", "output_http.so -w ./www -p 8080"
])
async def handle_client(websocket):
    async for message in websocket:
        if message == "MOVE FWD":
            set_motors(1,1,1,1, 0.5)
            print("received commands")
        else:
            print('invalid')

async def main():
    async with websockets.serve(handle_client, "0.0.0.0", 5000):
        await asyncio.Future()

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

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("stopped")
finally:
    set_motors(0,0,0,0)
    mjpg_process.terminate()
    