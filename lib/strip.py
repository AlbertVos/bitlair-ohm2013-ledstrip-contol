
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
import os


def signal_handler(_signal, _frame):
  """
  Signal handler to kill the application
  Usage: signal.signal(signal.SIGINT, signal_handler)
  """
  #print('Bye ...')
  strip.stop()
  os.kill(os.getpid(), signal.SIGKILL)
  sys.exit(0)

def toTuppleArray(string):
  """
  Convert string to array of tupples
  Parameter s can be:
    abcdef
    'abcdef'
    "abcdef"
    ("abcdef", 123)
    [("abcdef", 123)]
  """
  if ((string[0] == '"') or (string[0] == "'")):
    # String
    string = "[(" + string + ")]"
  elif not ((string[0] == '[') or (string[0] == '(')):
    # not an Array or Tuple
    string = "[('" + string + "',)]"
  elif string[0] == '(':
    # Tuple
    string = "[" + string + "]"
  else:
    pass
  return eval(string) # pylint: disable=eval-used


def getAddr(addr = None):
  defaultPort = 6454
  if addr and len(addr) > 0:
    pass
  else:
    # Check if addr= argument given or ADDR env. variable set
    if "ADDR" in os.environ:
      addr = toTuppleArray(os.environ.get('ADDR'))
    elif len(sys.argv) > 1:
      for i in range(1, len(sys.argv)):
        if sys.argv[i].startswith("addr="):
          addr = toTuppleArray(sys.argv[i][5:])
    else:
      addr = [("192.168.89.255", 6454)]
  # check for missing port and set to default
  for i, address in enumerate(addr):
    if len(address) == 1:
      addr[i] = (address[0], defaultPort)
  #print( "Addresses used:", addr )
  return addr


class Artnet:
  """
  The Artnet class provides operation for sending and receiving data
  using the Artnet protocol.
  """
  localHost = "0.0.0.0"
  localPort = 6454
  sock = 0
  fade = 1.0
  length = 170

  #                       01234567   8   9   a   b   c   d   e   f   10  11
  #                                  op-code protver seq phy universe len
  dataHeader = bytearray( b"Art-Net\x00\x00\x50\x00\x0e\x00\x00\x00\x00\x02\x00" )
  #                    01234567   8   9   a   b   c   d
  #                               op-code protver
  pollMsg = bytearray( b"Art-Net\x00\x00\x20\x00\x0e\x00\xff" )

  def __init__(self, addr = None):

    self.addr = getAddr(addr)

    if "FADE" in os.environ:
      self.fade = float(os.environ.get('FADE'))
      if self.fade > 1.0:
        self.fade = 1.0
      if self.fade < 0.0:
        self.fade = 0.0

    # Check if host= argument given or HOST env. variable set
    if len(sys.argv) > 1:
      for i in range(1, len(sys.argv)):
        if sys.argv[i].startswith("host="):
          self.localHost = sys.argv[i][5:]
    elif "HOST" in os.environ:
      self.localHost = os.environ.get('HOST')
    # Check if port= argument given or PORT env. variable set
    if len(sys.argv) > 1:
      for i in range(1, len(sys.argv)):
        if sys.argv[i].startswith("port="):
          self.localPort = int(sys.argv[i][5:])
    elif "PORT" in os.environ:
      self.localPort = int(os.environ.get('PORT'))

    # Create UDP socket
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    self.sock.bind((self.localHost, self.localPort))

  def close(self):
    """
    Shutdown the connection
    """
    self.clear()
    self.sock.close()

  def clear(self):
    """
    Clear the entire strip
    """
    data = self.dataHeader
    for _i in range(self.length):
      data += b"\x00\x00\x00"
    for _i, address in enumerate(self.addr):
      self.sock.sendto( data, address)

  def send(self, current_strip):
    """
    Send the data of a strip
    """
    data = bytearray(3*current_strip.length)
    for i in reversed(range(current_strip.length)):
      c = current_strip.get(current_strip.length - i)
      data[3*i+0] = int( c[0] * self.fade )
      data[3*i+1] = int( c[1] * self.fade )
      data[3*i+2] = int( c[2] * self.fade )
    for _i, address in enumerate(self.addr):
      self.sock.sendto( self.dataHeader + data, address)

  def poll(self):
    """
    Run poll for 5 seconds.
    """
    devices = []
    self.sock.setblocking(0)
    for _i, address in enumerate(self.addr):
      self.sock.sendto(self.pollMsg, address)
    print( "=== Sent artnet poll ===" )
    now = time.time()
    while (time.time() - now) < 5:
      ready = select.select([self.sock], [], [], 0.5)
      if ready[0]:
        rdata, raddr = self.sock.recvfrom(5000)
        if (rdata[8]) == 0x00 and (rdata[9]) == 0x20:
          print( "received poll request from", raddr[0], "@", raddr[1] )
          # officially this needs to be answered with a reply
        if (rdata[8]) == 0x00 and (rdata[9]) == 0x21:
          print( "received poll reply from", raddr[0], "@", raddr[1] )
          devices.append(raddr)
    self.sock.setblocking(1)
    return devices

strip = None

class Strip:
  """
  The Strip class defines operations for a 1-dimensional string of leds.
  """
  length = 0
  rgb = []

  def __init__(self, length, addr = None):
    """
    Constructor, creating a strip of length leds.
    """
    self.length = length
    self.clear()
    self.artnet = Artnet(addr)

    # ValueError: signal only works in main thread of the main interpreter
    try:
      signal.signal(signal.SIGINT, signal_handler)
    except ValueError as _e:
      pass

    global strip
    strip = self

  def stop(self):
    """
    Stop this strip
    """
    if "globalStop" in dir(strip):
      self.globalStop(self) # pylint: disable=no-member
    self.artnet.close()

  def send(self):
    """
    Send the data of myself to the strip
    """
    self.artnet.send(self)

  def clear(self, color = None):
    """
    Clear the entire strip with one color (default: black).
    Color is array: [r, g, b].
    """
    if color and len(color):
      [r, g, b] = color
    else:
      [r, g, b] = [0, 0, 0]
    self.rgb = [[r, g, b] for x in range(self.length)]

  def set(self, index, color, alpha = -1):
    """
    Set led at index to color.
    """
    if ((index >= 0) and (index < self.length)):
      [r, g, b] = color
      if alpha >= 0:
        c = self.get(index)
        if c[0] > 0 and c[1] > 0 and c[2] > 0:
          alpha = float(alpha) / 255.0
          r = int(alpha * r + (1 - alpha) * c[0])
          g = int(alpha * g + (1 - alpha) * c[1])
          b = int(alpha * b + (1 - alpha) * c[2])
          if r > 255:
            r = 255
          if g > 255:
            g = 255
          if b > 255:
            b = 255
      self.rgb[self.length - 1 - index] = [r, g, b]

  def get(self, index):
    """
    Get color of led at index.
    """
    if ((index >= 0) and (index < self.length)):
      [r, g, b] = self.rgb[self.length - 1 - index]
      return [r, g, b]
    else:
      return [0, 0, 0]

  def setm(self, index, colors):
    """
    Set a range of leds starting at index to the specified colors.
    """
    length = len(colors)
    for i in range(length):
      self.set(index + i, colors[i])

  def getm(self, index, length):
    """
    Get the colors of a range of leds starting at index up to given length.
    """
    a = []
    for i in range(length):
      a.append(self.get(index + i))
    return a

  def fade(self, a):
    """
    Fade that strip by a factor a
    """
    for i in range(self.length):
      [r, g, b] = self.rgb[i]
      r = int(float(r) * float(a))
      g = int(float(g) * float(a))
      b = int(float(b) * float(a))
      self.rgb[i] = [r, g, b]

  def print_(self):
    """
    Print strip contents to stdout.
    """
    for i in range(self.length):
      print("strip ", i, self.rgb[i][0], self.rgb[i][1], self.rgb[i][2])



class Strip2D:
  """
  The Strip2D class defines operations on a 2-dimensional led banner and
  maps it to a Strip.
  This can be initialized in 2 ways.

  1. for a cylinder, 7 pixels circumference,
     21 pixels high spiral from top to bottom clockwise (from top):
  s = Strip2D(7, 21)

  2. for a cone, with 6 pixels circumference,
     arbitrary heights (max. 21) zig-zag from bottom to top clockwise (from top):
  s = Strip2D( 21, 18, 17, 15, 15, 17 )

  Note that the zig-zag style cannot use any of the `rot*` methods
  since moving from one height to a different will cause loss of pixel information
  """
  lenx = 0
  leny = 0
  lengths = None
  fadeCount = 0
  strip = None

  def __init__(self, lenx, leny, *args, addr=None):
    """Constructor, defining a led banner of width lenx and height leny."""

    if len( args ) > 0:
      # Vertical zig-zag string of lengths
      self.lengths = []
      self.lengths.append( lenx )
      self.lengths.append( leny )
      if lenx > leny:
        self.leny = lenx
      else:
        self.leny = leny

      for arg in args:
        self.lengths.append( arg )
        if arg > self.leny:
          self.leny = arg
      self.lenx = len( self.lengths )
    else:
      # Regular (spiral) layout
      self.lenx = lenx
      self.leny = leny
    #self.strip = Strip(lenx * leny, addr)
    self.strip = Strip(150, addr)
    #self.f = [.20 * math.sin(math.pi * i / 26) for i in range(1, 12)]
    self.f = [0.02, 0.03, 0.05, 0.09, 0.10, 0.11, 0.12, 0.13, 0.17, 0.19, 0.20]

  def send(self):
    """Send data to the strip"""
    if not self.lengths:
      for i in range(self.lenx * self.leny, self.strip.length):
        self.strip.set(i, [0, 0, 0])
    self.strip.send()

  def set(self, x, y, color):
    """Set the color of the led at (x, y)."""
    if self.lengths:
      # Vertical zig-zag string of lengths
      if x >= len(self.lengths):
        return
      if y > self.lengths[x]:
        return

      pos = 149
      for hor in range(x):
        pos -= self.lengths[hor]
      if x % 2 == 0:
        pos -= y
      else:
        pos += y - self.lengths[x] + 1

    else:
      # Regular (spiral) layout
      pos = x + y * self.lenx

    self.strip.set(pos, color)

  def get(self, x, y):
    """Get the color of the led at (x, y)."""
    if self.lengths:
      # Vertical zig-zag string of lengths
      pos = 0
      if x % 2 == 0:
        pos += self.lengths[x]
        pos -= y - 1
      else:
        pos += y
      pos += 51
    else:
      # Regular (spiral) layout
      pos = x + y * self.lenx
    return self.strip.get(pos)

  def rotr(self):
    """
    Rotate the banner contents 1 led to the right.
    """
    for y in range(self.leny):
      c = self.get(self.lenx - 1, y)
      for x in reversed(range(self.lenx - 1)):
        self.set(x + 1, y, self.get(x, y))
      self.set(0, y, c)

  def rotl(self):
    """
    Rotate the banner contents 1 led to the left.
    """
    for y in range(self.leny):
      c = self.get(0, y)
      for x in range(self.lenx - 1):
        self.set(x, y, self.get(x + 1, y))
      self.set(self.lenx - 1, y, c)

  def rotu(self):
    """
    Rotate the banner contents 1 led up.
    """
    c = self.strip.getm((self.leny - 1) * self.lenx, self.lenx)
    for y in reversed(range(self.leny - 1)):
      self.strip.setm((y + 1) * self.lenx, \
        self.strip.getm(y * self.lenx, self.lenx))
    self.strip.setm(0, c)

  def rotd(self):
    """
    Rotate the banner contents 1 led down.
    """
    c = self.strip.getm(0, self.lenx)
    for y in range(self.leny - 1):
      self.strip.setm(y * self.lenx, \
        self.strip.getm((y + 1) * self.lenx, self.lenx))
    self.strip.setm((self.leny - 1) * self.lenx, c)

  def pattern(self, data, step):
    """
    Set pattern for every y increment with step.
    """
    #length = len(data)
    for y in range(self.leny):
      for x in range(self.lenx):
        self.set(x, y, data[(x + y * step) % self.lenx])

  def fade(self, a):
    """
    Fade that strip by a factor a
    """
    for y in range(self.leny):
      for x in range(self.lenx):
        p = self.get(x, y)
        p[0] = int(float(p[0]) * float(a))
        p[1] = int(float(p[1]) * float(a))
        p[2] = int(float(p[2]) * float(a))
        self.set(x, y, p)

  def coneFade(self, yy):
    for y_position in range(self.leny):
      if abs(y_position - yy) >= len(self.f):
        f = self.f[len(self.f) - 1]
      else:
        f = self.f[abs(y_position - yy)]
      for x_position in range(self.lenx):
        c = self.get(x_position, y_position)
        c = [int(c[0] * f), int(c[1] * f), int(c[2] * f)]

        self.set(x_position, y_position, c)
        self.set(x_position, y_position, c)


class Canvas:
  """
  The Canvas class provides function for drawing on a Strip2D.
  """
  lenx = 0
  leny = 0
  strip2D = 0

  def __init__(self, lenx, leny):
    self.lenx = lenx
    self.leny = leny
    self.strip2D = Strip2D(lenx, leny)

  def circle(self, cx, cy, radius, color):
    """
    Draw a circle
    """
    x = 0
    y = radius
    p = (5 - radius * 4) / 4
    self.circle_points(cx, cy, x, y, color)
    while x < y:
      x += 1
      if p < 0:
        p += 2 * x + 1
      else:
        y -= 1
        p += 2 * (x - y) + 1
      self.circle_points(cx, cy, x, y, color)

  def circle_points(self, cx, cy, x, y, c):
    """
    used by circle; do not use
    """
    if x == 0:
      self.strip2D.set(cx, cy + y, c)
      self.strip2D.set(cx, cy - y, c)
      self.strip2D.set(cx + y, cy, c)
      self.strip2D.set(cx - y, cy, c)
    elif x == y:
      self.strip2D.set(cx + x, cy + y, c)
      self.strip2D.set(cx - x, cy + y, c)
      self.strip2D.set(cx + x, cy - y, c)
      self.strip2D.set(cx - x, cy - y, c)
    elif x < y:
      self.strip2D.set(cx + x, cy + y, c)
      self.strip2D.set(cx - x, cy + y, c)
      self.strip2D.set(cx + x, cy - y, c)
      self.strip2D.set(cx - x, cy - y, c)
      self.strip2D.set(cx + y, cy + x, c)
      self.strip2D.set(cx - y, cy + x, c)
      self.strip2D.set(cx + y, cy - x, c)
      self.strip2D.set(cx - y, cy - x, c)


class Effect(object):
  quit = False
  count = 0

  def __init__(self, strip2D):
    self.strip2D = strip2D

  """
    You can either override the run method or the step method.
    If you override the run method you have to do everything yourself.
    The step method is called repeatedly with a sleep of .02
    in between; the strip send method is called automatically.
  """
  def run(self, runtime = None ):
    if runtime is None:
      if hasattr( sys, "maxint" ): # Python 2
        runtime = sys.maxint
      elif hasattr( sys, "maxsize" ): # Python 3
        runtime = sys.maxsize

    self.strip2D.strip.clear([0, 0, 0])
    self.strip2D.send()

    self.quit = False
    now = time.time()
    self.init()
    while (not self.quit) and ((time.time() - now) < runtime):
      self.step(self.count)
      self.count += 1
      self.strip2D.send()
      time.sleep(0.02)

  """
    init is called be a new sequence of steps is executed to reinitialize.
  """
  def init(self):
    return

  def step(self, count):
    raise Exception("run method not implemented!!")


"""

'Art-Net\x00\x00\x21\xc0\xa8Y\x806\x19\x059\x00\x07\x00\x00\x00\x00LOLED strip\x00\x00\x00\x00\x00\x00\x00\x00\x00LED strip controller for OHM 2013\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0f\x00\x00\x00\x00\x00\x00\x00\x00\x00\xcc\xb5Z\x00\x00U\xc0\xa8Y\x80\x00p\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'


opcode  ip  .   .   .   port.   version
'Art-Net\x00\x00\x21\x00\x00\x00\x00\x36\x19\x00\x00\x00\x07\x00\x00\x00\x00LOLED strip\x00\x00\x00\x00\x00\x00\x00\x00\x00LED strip controller for OHM 2013\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0f\x00\x00\x00\x00\x00\x00\x00\x00\x00\xcc\xb5Z\x00\x00U\xc0\xa8Y\x80\x00p\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'


"""
