#!/usr/bin/env python3
"""
  Poll all available poles and give them a color, so you can determine the
  order of the ip addresses to the physical location.
"""

import time
import sys
sys.path.append('../lib')
from strip import Strip

color = [
  [35, 17, 5],
  [255, 0, 0],
  [255, 80, 0],
  [255, 255, 0],
  [0, 255, 0],
  [0, 0, 255],
  [128, 0, 128],
  [50, 50, 50],
  [255, 255, 255],
  ]

colornames = [
  "brown",
  "red",
  "orange",
  "yellow",
  "green",
  "blue",
  "purple",
  "gray"
  "white",
  ]

def scan():
  strip = Strip(150)

  while True:
    strip.artnet.addr = [("192.168.89.255", 6454)]
    devices = strip.artnet.poll()
    print( devices )
    for i, device in enumerate(devices):
      strip.artnet.addr = [device]
      strip.clear(color[i])
      strip.send()
      print( "-> ", device, color[i], colornames[i] )
      time.sleep(.1)
    time.sleep(10)

scan()
