import time
from math import sin, cos
import random
import usb_hid
from hid_gamepad import Gamepad
from ppm_decoder import get_ppm_frame

gp = Gamepad(usb_hid.devices)

time.sleep(0.5)

throttleid = 7
turnid     = 5
spinid     = 1
flipid     = 3

def map_value(x, in_min=499, in_max=1500, out_min=-125, out_max=125):
    # Clamp input
    if x < in_min:
        x = in_min
    elif x > in_max:
        x = in_max

    # Linear mapping
    return int((x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min)


while True:
    ch = get_ppm_frame()
    throttle = ch[throttleid]
    turn = ch[turnid]
    spin = ch[spinid]
    flip = ch[flipid]
    
    x = map_value(throttle)
    y = map_value(turn)
    z = map_value(spin)
    rz = map_value(flip)
    gp.move_joysticks(x=x, y=-y, z=z, r_z=rz)
    time.sleep(0.01)
