#!/usr/bin/env python3

# TODO: barber pole downward (led 1,7,13...)
# downward (bloodletting)
# red: (arterial) blood -> surgeon
# blue: (venous blood) barber -> 
# white: bandage
 
# https://www.wondersandmarvels.com/2011/10/a-history-of-the-barbers-pole.html

import time

import sys
sys.path.append('../lib')
from strip import *

#Strip -> 
#    self.strip = Strip(150, addr)
#  self.strip.send()
# self.strip.length):
# .strip.set(i, [0, 0, 0])
    



class Barber(Effect):
  def __init__(self, strip2D, colors):
    super(Barber, self).__init__(strip2D)
    self.strip2D.strip.clear()
    self.colors = colors

  def run(self, runtime = None):
    if ( runtime == None ):
         if ( hasattr( sys, "maxint" ) ): # Python 2
            runtime = sys.maxint
         elif ( hasattr( sys, "maxsize" ) ): # Python 3
            runtime = sys.maxsize
        
    now = time.time()
    offset = 0
    while (not self.quit) and ((time.time() - now) < runtime):
    
      for i in range(self.strip2D.strip.length):
        self.strip2D.strip.set(i, self.colors[offset])
        offset += 1
        if ( offset >= len(self.colors) ):
          offset = 0
      self.strip2D.send()
      
      time.sleep(0.20)
      offset += 1
      if ( offset >= len(self.colors) ):
        offset = 0

    self.quit = False



"""
./barber.py addr=192.168.1.255
./barber.py [surgeon|barber] 'addr=[("192.168.1.255", ), ("localhost", 7000)]'
./barber.py [1|2|3] 'addr=[("192.168.1.255", 6454), ("localhost", 7000)]'
"""

if __name__ == "__main__":
  red = [255,   0,   0] 
  white = [64, 64, 64]
  blue = [  0,   0, 255]

  if (len(sys.argv) >= 2 and sys.argv[1] == "surgeon"):
    e = Barber(Strip2D(7, 21), [ red, white, white ] )
  elif (len(sys.argv) >= 2 and sys.argv[1] == "barber"):
    e = Barber(Strip2D(7, 21), [ blue, white, white ] )
  else:
    # Modern (patriot) style
    e = Barber(Strip2D(7, 21), [ red, white, white, blue, white, white ] )
  e.run()


