#!/usr/bin/env python3

"""
Start one window listening at port 7000
  ./simstrip.py
Start 2 window listening at port 7000 and 7001
  ./simstrip.py 2 port=7000
"""

import os
import select
import socket
import subprocess
import sys
import time
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame


portDefault = 7000

PIXELSIZE = 40 #20

class SimStrip:
  port = 0
  sock = 0
  screen = object()

  def __init__(self, port = portDefault):
    # Check if port= argument given or PORT env. variable set
    if port == portDefault:
      if "PORT" in os.environ:
        port = int(os.environ.get('PORT'))
      for i in range(1, len(sys.argv)):
        if sys.argv[i].startswith("port="):
          port = int(sys.argv[i][5:])

    self.port = port
    print( "SimStrip using port: ", self.port )
    sys.stdout.flush()

    # Create UDP socket
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    self.sock.bind(("0.0.0.0", self.port))

    #self.screen = Screen("Strip " + str(self.port % 100 + 1))
    self.screen = Screen("@" + str(self.port))

  # Shutdown the connection
  def close(self):
    self.sock.close()

  def handleMessages(self):
    self.sock.setblocking(0)
    while True:
      self.screen.processEvents()
      ready = select.select([self.sock], [], [], 0.01)
      if ready[0]:
        rdata, addr = self.sock.recvfrom(5000)
        #print "received data from", addr[0], "@", addr[1], len(rdata)
        #self.hexdump(rdata)
        if rdata[8] == 0x00 and rdata[9] == 0x20:
          print( "received poll request from", addr[0], "@", addr[1] )
          # officially this needs to be answered with a reply
        if rdata[8] == 0x00 and rdata[9] == 0x21:
          # Ignore for now
          # print "received poll reply from", addr[0], "@", addr[1]
          pass
        if rdata[8] == 0x00 and rdata[9] == 0x50:
          #print "received data from", addr[0], "@", addr[1], len(rdata)

          # draw pixels
          #l = len(rdata) - 18
          for i in range(0, 7 * 21):
            x = 6 - (i % 7)
            y = int(i / 7)
            r = rdata[18 + 3 * i + 9]
            g = rdata[18 + 3 * i + 1 + 9]
            b = rdata[18 + 3 * i + 2 + 9]
            self.screen.draw(x, y, (r, g, b))

          self.screen.updateScreen()

    self.sock.setblocking(1)

  def hexdump(self, data):
    print( ":".join("{:02x}".format(ord(c)) for c in data) ) # pylint: disable=consider-using-f-string

class Screen:
  def __init__(self, title):

    self.pixelswide = 7
    self.pixelshigh = 21

    self.screenwide = PIXELSIZE * self.pixelswide
    self.screenhigh = PIXELSIZE * self.pixelshigh

    self.screen = pygame.display.set_mode((self.screenwide, self.screenhigh))
    pygame.display.set_caption(title)
    self.surface = pygame.Surface((self.pixelswide, self.pixelshigh))

  def processEvents(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        sys.exit()

  def updateScreen(self):
    pygame.transform.scale(self.surface, \
      (self.screenwide,self.screenhigh), self.screen)
    pygame.display.update()
    self.surface.fill((0, 0, 0))

  def draw(self, x, y, rgb):
    self.surface.set_at((x, y), rgb)


def run(port):
  pygame.init()
  ss = SimStrip(port)
  ss.handleMessages()


def start(port, num):
  for i in range(num):
    pos_x = 100 + 100 * i
    pos_y = 100
    os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (pos_x,pos_y) # pylint: disable=consider-using-f-string
    os.environ['SDL_VIDEO_CENTERED'] = '0'
    subprocess.Popen(["python3", "simstrip.py", str(port + i), "-"])
    time.sleep(0.3)


if __name__ == "__main__":
  num = 1
  isChild = False

  for i in range(1, len(sys.argv)):
    if sys.argv[i].startswith("port="):
      portDefault = int(sys.argv[i][5:])
      #print "port =", portDefault
    elif sys.argv[i] == "-":
      isChild = True
    #elif sys.argv[i].startswith("num="):
    else:
      n = int(sys.argv[i])
      if n > 1 and n < 20:
        num = n
      #print "num =", num

  if isChild:
    port = int(sys.argv[1])
    #print "port =", port
    run(port)
  else:
    start(portDefault, num)
