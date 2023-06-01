#!/usr/bin/env python3

import time

import sys
import signal
from threading import Semaphore, Thread, Event
sys.path.append('../lib')
from strip import Effect, Strip2D

# Primary semaphore: first to get priority
sema_prepare = Semaphore()
# Actual green light semaphore
sema_go = Semaphore()

off = [ 0, 0, 0 ]
red = [ 255, 0, 0 ]
yellow = [ 255, 96, 0 ]
green = [ 0, 255, 0 ]

# Lights go from bottom to top
none = [ off, off, off ]
alllights = [ green, yellow, red ]

traffic_stop = [ off, off, red ]
traffic_prepare = [ off, off, red ] # choose between [ off, yellow, red ] or just [ off, off, red ]
go = [ green, off, off ]
traffic_caution = [off, yellow, off ]

bridge_closed_indefinitely = [ red, off, red ]
bridge_closed = [ off, off, red ]
bridge_prepare = [ off, green, red ]
bridge_go = [ off, green, off ]
bridge_caution = [ off, off, red ]

# TODO: automated (orange) with 2-way boats
bridge = [
            [ bridge_closed, 5, sema_go ] ,
            [ bridge_prepare, 3.5, sema_prepare ],
            [ bridge_go, 5, sema_go ],
            [ bridge_caution, 3.5, sema_prepare ]
          ]

# Yellow light duration:
# @80km/h → 5s
# @70km/h → 4.5s
# @50km/h → 3.5s
# overlap stop time, stop+time, prepare+time, go+time, caution+time
traffic = [
            [ traffic_stop, 0, sema_go ],           # intersection release time (all red)
            [ traffic_prepare, 1.5, sema_prepare ], # prepare time (see next NOTE)
            [ go, 5, sema_go ],                     # green time
            [ traffic_caution, 3.5, sema_prepare ]  # orange time
          ]
# NOTE: prepare time is calculated as a remainder of caution+stop time
traffic[1][1] = max( traffic[0][1] + traffic[3][1] - traffic[1][1], 0 )

# https://wetten.overheid.nl/BWBR0009151/2019-07-01 section 114
# De frequentie van het knipperen bedraagt minimaal 40 en maximaal 60 onderbrekingen per minuut
# met een licht-donkerverhouding van 1:1.
disabled = [
    [ traffic_caution, 1.1, None ],
    [ none, 1.1, None ]
  ]

# Define the actual program here (traffic, disabled, bridge)
program = traffic

class Trafficlight(Effect):

  sleepEvent = None
  _quit = False

  @property
  def quit(self):
    return self._quit

  @quit.setter
  def quit(self, value):
    self._quit = value
    # Kill the timer if we want to quit
    if value:
      print( "stopping timer" )
      self.sleepEvent.set()

  def __init__(self, strip2D):
    super().__init__(strip2D)

    self.strip2D.strip.globalStop = self.globalStop

    addr = self.strip2D.strip.artnet.addr

    self.extraLights = []
    if len(addr) > 1:
      for i in range(1, len(addr)):
        stripCopy = Strip2D(7, 21)
        stripCopy.strip.artnet.addr = [addr[i]]
        self.extraLights.append( Trafficlight(stripCopy) )
    self.strip2D.strip.artnet.addr = [addr[0]]

  # Set the actual light
  def setLight( self, lights ):
    self.strip2D.strip.clear()

    offset = -1
    for y in range(self.strip2D.leny):
      if y % 7 == 0:
        offset += 1
      for x in range(int(self.strip2D.lenx / 7 * 3)):
        self.strip2D.set(x+0-offset, y, lights[offset])

    self.strip2D.send()
  def globalStop(self):
    pass

  def run(self, runtime = None):
    self.sleepEvent = Event()

    if runtime is None:
      if hasattr( sys, "maxint" ): # Python 2
        runtime = sys.maxint
      elif hasattr( sys, "maxsize" ): # Python 3
        runtime = sys.maxsize

    # Don't use globalStop since apparently it is a child thread
    # which has no control over the main thread.
    try:
      signal.signal(signal.SIGINT, self.signal_handler)
    except ValueError as _e:
      # Will catch the error if a thread tries to subscribe
      pass

    # Start with red
    self.setLight( program[0][0] )

    # Run the secondary lights
    for light in self.extraLights:
      thread = Thread(target = light.run, args = [])
      thread.daemon = True
      light.thread = thread
      thread.start()

    now = time.time()
    while (not self.quit) and ((time.time() - now) < runtime):
      if program[1][2] is not None:
        program[1][2].acquire() # pylint: disable=consider-using-with
      self.sleepEvent.wait( program[1][1] ) # prepare delay (warn+stop taken into account)
      self.setLight( program[1][0] ) # prepare

      if len( program ) > 2:
        if program[2][2] is not None:
          program[2][2].acquire() # pylint: disable=consider-using-with
        self.setLight( program[2][0] ) # go
        self.sleepEvent.wait( program[2][1] ) # go delay

        self.setLight( program[3][0] ) # warning
        if program[3][2] is not None:
          program[3][2].release()
        self.sleepEvent.wait(program[3][1]) # warn delay

      if len( program ) <= 2:
        self.sleepEvent.wait(program[0][1]) # stop overlap delay
      self.setLight( program[0][0] ) # stop
      if len( program ) > 2:
        self.sleepEvent.wait(program[0][1]) # stop overlap delay
      if program[0][2] is not None:
        program[0][2].release()

    print( "stopping light" )
    for light in self.extraLights:
      print( light )
      # Restore addresses
      self.strip2D.strip.artnet.addr.append(light.strip2D.strip.artnet.addr[0])
      light.quit = True
      light.sleepEvent.set()
      light.thread.join()
    self.strip2D.strip.clear()
    self.strip2D.send()
    time.sleep(0.001) # yield (allow sending the packet)

    self.quit = False

  def signal_handler(self, _signal, _frame):
    """
    Signal handler to kill the application
    Usage: signal.signal(signal.SIGINT, signal_handler)
    """
    print('We got signal..')
    self.quit = True

    for light in self.extraLights:
      light.quit = True


if __name__ == "__main__":
  e = Trafficlight(Strip2D(7, 21))
  e.run()
