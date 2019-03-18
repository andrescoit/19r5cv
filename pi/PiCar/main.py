import RPi.GPIO as gpio
import time
import sys
import Tkinter as tk
from sensor import distance

def init():
    gpio.setmode(gpio.BCM)
    gpio.setup(17, gpio.OUT)
    gpio.setup(18, gpio.OUT)

def stop(tf):
    gpio.output(7, False)
    gpio.output(11, False)
    time.sleep(tf)

def forward(tf):
    gpio.output(7, True)
    gpio.output(11, True)
    time.sleep(tf)

def turn_right(tf):
    gpio.output(7, True)
    gpio.output(11, False)
    time.sleep(tf)

def turn_left(tf):
    gpio.output(7, False)
    gpio.output(11, True)
    time.sleep(tf)

def key_input(Event):
    init()
    print "Key:", event.char
    key_press = event.char
    sleep_time = 0.060

    if key_press.lower() == "w":
       forward(sleep_time)
    elif key_press.lower() == "a":
       turn_left(sleep_time) 
    elif key_press.lower() == "d":
       turn_right(sleep_time)
    elif key_press.lower() == "s":
       stop(sleep_time)
    else:
 	pass
  
    curDis = distance("cm")
    print("Distance:", curDis)

    if curDis <15:
       init()
       reverse(0.5)

command = tk.TK()
command.bind('<keypress>', key_input)
command.mainloop()

gpio.cleanup()
