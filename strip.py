
"""
# default values -> broadcast at 192.168.89.255 from port 6454
./<app>.py
# broadcast at 192.168.1.255
./<app>.py addr=192.168.1.255
# send to multiple addresses (first with default port 6454).
./<app>.py 'addr=[("192.168.1.255",),("localhost",7000)]'

or set environment parameter ADDR:
export ADDR=192.168.1.255
export ADDR='[("192.168.1.255",),("localhost",7000)]'
"""


import socket
import time
import signal
import sys
import select
import threading
import os
import random
import math


# Signal handler to kill the application
# Usage: signal.signal(signal.SIGINT, signal_handler)

def signal_handler(signal_, frame):
  #print('Bye ...')
  strip.stop();
  os.kill(os.getpid(), signal.SIGKILL);
  sys.exit(0)

# Convert string to array of tupples
# Parameter s can be:
#   abcdef 
#   'abcdef' 
#   "abcdef" 
#   ("abcdef", 123)
#   [("abcdef", 123)] 
   
def toTuppleArray(s):
  if ((s[0] == '"') or (s[0] == "'")):
    s = "[(" + s + ")]";
  elif not ((s[0] == '[') or (s[0] == '(')):
    s = "[('" + s + "',)]";
  elif s[0] == '(':
    s = "[" + s + "]";
  else:
    pass;
  r = eval(s);
  return eval(s);


#
# The Artnet class provides operation for sending and receiving data
# using the Artnet protocol.
#

class Artnet:
  localHost = "0.0.0.0";
  localPort = 6454;
  addr = [("192.168.89.255", 6454)];
  sock = 0;

  #                       01234567   8   9   a   b   c   d   e   f   10  11  
  #                                  op-code protver seq phy universe len  
  dataHeader = bytearray("Art-Net\x00\x00\x50\x00\x0e\x00\x00\x00\x00\x02\x00")
  #                    01234567   8   9   a   b   c   d
  #                               op-code protver 
  pollMsg = bytearray("Art-Net\x00\x00\x20\x00\x0e\x00\xff");

  def __init__(self, addr_ = []):

    if len(addr_) > 0:
      self.addr = addr_;
    else:
      # Check if addr= argument given or ADDR env. variable set
      if "ADDR" in os.environ:
        self.addr = toTuppleArray(os.environ.get('ADDR'));
      if len(sys.argv) > 1:
        for i in range(1, len(sys.argv)):
          if sys.argv[i].startswith("addr="):
            self.addr = toTuppleArray(sys.argv[i][5:]);

    # check for missing port and set to default
    for i in range(len(self.addr)):
      if len(self.addr[i]) == 1:
        self.addr[i] = (self.addr[i][0], self.localPort);

    #print "Artnet addresses:", self.addr;

    # Check if host= argument given or HOST env. variable set
    if len(sys.argv) > 1:
      for i in range(1, len(sys.argv)):
        if sys.argv[i].startswith("host="):
          self.localHost = sys.argv[i][5:];
    elif "HOST" in os.environ:
      self.localHost = os.environ.get('HOST');
    # Check if port= argument given or PORT env. variable set
    if len(sys.argv) > 1:
      for i in range(1, len(sys.argv)):
        if sys.argv[i].startswith("port="):
          self.localPort = int(sys.argv[i][5:]);
    elif "PORT" in os.environ:
      self.localPort = int(os.environ.get('PORT'));

    # Create UDP socket
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
    self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1);
    self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1);
    self.sock.bind((self.localHost, self.localPort));

  # Shutdown the connection
  def close(self):
    self.clear();
    self.sock.close();

  # Clear the entire strip
  def clear(self):
    data = '';
    c = [0, 0, 0];
    for i in range(150):
      data += chr(c[0]) + chr(c[1]) + chr(c[2]);
    for i in range(len(self.addr)):
      self.sock.sendto(self.dataHeader + data, self.addr[i])

  # Send the data of a strip
  def send(self, strip):
    data = '';
    for i in reversed(range(strip.length)):
      c = strip.get(i);
      #print "send ", i, str(c[0]), str(c[1]), str(c[2]);
      data += chr(c[0]) + chr(c[1]) + chr(c[2]);
    #time.sleep(0.02)
    for i in range(len(self.addr)):
      self.sock.sendto(self.dataHeader + data, self.addr[i])

  # Run poll for 10 seconds.
  def poll(self):
    self.sock.setblocking(0)
    for i in range(len(self.addr)):
      self.sock.sendto(self.pollMsg, self.addr[i])
    print "=== Sent artnet poll ==="
    now = time.time();
    while (time.time() - now) < 10:
      ready = select.select([self.sock], [], [], 0.5)
      if ready[0]:
        rdata, raddr = self.sock.recvfrom(5000)
        if ord(rdata[8]) == 0x00 and ord(rdata[9]) == 0x20:
          print "received poll request from", raddr[0], "@", raddr[1];
          # officially this needs to be answered with a reply
        if ord(rdata[8]) == 0x00 and ord(rdata[9]) == 0x21:
          print "received poll reply from", raddr[0], "@", raddr[1];
    self.sock.setblocking(1)

#
# The Strip class defines operations for a 1-dimensional string of leds.
#

class Strip:
  length = 0
  rgb = []

  # Constructor, creating a strip of length leds.
  def __init__(self, length, addr = []):
    self.length = length;
    self.clear()
    self.artnet = Artnet(addr);
    
    signal.signal(signal.SIGINT, signal_handler)

    global strip;
    strip = self;

  # Stop this strip
  def stop(self):
    self.artnet.close();

  # Send the data of myself to the strip
  def send(self):
    self.artnet.send(self);
    
  # Clear the entire strip with one color (default: black).
  # Color is array: [r, g, b].
  def clear(self, color = [0, 0, 0]):
    [r, g, b] = color;
    self.rgb = [[r, g, b] for x in range(self.length)];

  # Set led at index to color.
  def set(self, index, color):
    if ((index >= 0) and (index < self.length)):
      [r, g, b] = color;
      self.rgb[self.length - 1 - index] = [r, g, b];

  # Get color of led at index.
  def get(self, index):
    if ((index >= 0) and (index < self.length)):
      [r, g, b] = self.rgb[self.length - 1 - index]
      return [r, g, b];
    else:
      return [0, 0, 0];

  # Set a range of leds starting at index to the specified colors.
  def setm(self, index, colors):
    length = len(colors);
    for i in range(length):
      self.set(index + i, colors[i]);

  # Get the colors of a range of leds starting at index up to given length.
  def getm(self, index, length):
    a = [];
    for i in range(length):
      a.append(self.get(index + i));
    return a;

  # Fade that strip by a factor a
  def fade(self, a):
    for i in range(self.length):
      [r, g, b] = self.rgb[i];
      r = int(float(r) * float(a));
      g = int(float(g) * float(a));
      b = int(float(b) * float(a));
      self.rgb[i] = [r, g, b];

  # Print strip contents to stdout.
  def print_(self):
    for i in range(self.length):
      print("strip ", i, self.rgb[i][0], self.rgb[i][1], self.rgb[i][2]);


#
# The Strip2D class defines operations on a 2-dimensional led banner and
# maps it to a Strip.
#

class Strip2D:
  lenx = 0;
  leny = 0;
  fadeCount = 0;
  global strip

  # Constructor, defining a led banner of width lenx and height leny.
  def __init__(self, lenx, leny, addr = []):
    self.lenx = lenx;
    self.leny = leny;
    self.strip = Strip(lenx * leny, addr);

  # Send data to the strip
  def send(self):
    self.strip.send();

  # Set the color of the led at (x, y).
  def set(self, x, y, color):
    self.strip.set(x + y * self.lenx, color);

  # Get the color of the led at (x, y).
  def get(self, x, y):
    return self.strip.get(x + y * self.lenx);

  # Rotate the banner contents 1 led to the right.
  def rotr(self):
    for y in range(self.leny):
      c = self.get(self.lenx - 1, y);
      for x in reversed(range(self.lenx - 1)):
        self.set(x + 1, y, self.get(x, y));
      self.set(0, y, c);

  # Rotate the banner contents 1 led to the left.
  def rotl(self):
    for y in range(self.leny):
      c = self.get(0, y);
      for x in range(self.lenx - 1):
        self.set(x, y, self.get(x + 1, y));
      self.set(self.lenx - 1, y, c);

  # Rotate the banner contents 1 led up.
  def rotu(self):
    c = self.strip.getm((self.leny - 1) * self.lenx, self.lenx);
    for y in reversed(range(self.leny - 1)):
      self.strip.setm((y + 1) * self.lenx, \
        self.strip.getm(y * self.lenx, self.lenx));
    self.strip.setm(0, c);

  # Rotate the banner contents 1 led down.
  def rotd(self):
    c = self.strip.getm(0, self.lenx);
    for y in range(self.leny - 1):
      self.strip.setm(y * self.lenx, \
        self.strip.getm((y + 1) * self.lenx, self.lenx));
    self.strip.setm((self.leny - 1) * self.lenx, c);

  # Set pattern for every y increment with step.
  def pattern(self, data, step):
    length = len(data);
    for y in range(self.leny):
      for x in range(self.lenx):
        self.set(x, y, data[(x + y * step) % self.lenx]);

  # Fade that strip by a factor a
  def fade(self, a):
    for y in range(self.leny):
      for x in range(self.lenx):
        p = self.get(x, y);
        p[0] = int(float(p[0]) * float(a));
        p[1] = int(float(p[1]) * float(a));
        p[2] = int(float(p[2]) * float(a));
        self.set(x, y, p);


#
# The Canvas class provides function for drawing on a Strip2D.
#

class Canvas:
  lenx = 0;
  leny = 0;
  strip2D = 0; 

  def __init__(self, lenx, leny):
    self.lenx = lenx;
    self.leny = leny;
    self.strip2D = Strip2D(lenx, leny);

  # Draw a circle
  def circle(self, cx, cy, radius, color):
    x = 0;
    y = radius;
    p = (5 - radius * 4) / 4;
    self.circlePoints(cx, cy, x, y, color);
    while (x < y):
      x += 1;
      if (p < 0):
        p += 2 * x + 1;
      else:
        y -= 1;
        p += 2 * (x - y) + 1;
      self.circlePoints(cx, cy, x, y, color);

  # used by circle; do not use
  def circlePoints(self, cx, cy, x, y, c):
    if (x == 0):
      self.strip2D.set(cx, cy + y, c);
      self.strip2D.set(cx, cy - y, c);
      self.strip2D.set(cx + y, cy, c);
      self.strip2D.set(cx - y, cy, c);
    elif (x == y):
      self.strip2D.set(cx + x, cy + y, c);
      self.strip2D.set(cx - x, cy + y, c);
      self.strip2D.set(cx + x, cy - y, c);
      self.strip2D.set(cx - x, cy - y, c);
    elif (x < y):
      self.strip2D.set(cx + x, cy + y, c);
      self.strip2D.set(cx - x, cy + y, c);
      self.strip2D.set(cx + x, cy - y, c);
      self.strip2D.set(cx - x, cy - y, c);
      self.strip2D.set(cx + y, cy + x, c);
      self.strip2D.set(cx - y, cy + x, c);
      self.strip2D.set(cx + y, cy - x, c);
      self.strip2D.set(cx - y, cy - x, c);


class Effect(object):
  quit = False;

  def __init__(self, strip2D):
    self.strip2D = strip2D;

  def run():
    raise Exception("run method not implemented!!");




"""

'Art-Net\x00\x00\x21\xc0\xa8Y\x806\x19\x059\x00\x07\x00\x00\x00\x00LOLED strip\x00\x00\x00\x00\x00\x00\x00\x00\x00LED strip controller for OHM 2013\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0f\x00\x00\x00\x00\x00\x00\x00\x00\x00\xcc\xb5Z\x00\x00U\xc0\xa8Y\x80\x00p\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'


opcode  ip  .   .   .   port.   version
'Art-Net\x00\x00\x21\x00\x00\x00\x00\x36\x19\x00\x00\x00\x07\x00\x00\x00\x00LOLED strip\x00\x00\x00\x00\x00\x00\x00\x00\x00LED strip controller for OHM 2013\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0f\x00\x00\x00\x00\x00\x00\x00\x00\x00\xcc\xb5Z\x00\x00U\xc0\xa8Y\x80\x00p\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'


"""


