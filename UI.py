#!/usr/bin/env python3
import os
import sys
import re
import termios
import fcntl
from glob import glob
from threading import Thread
from importlib import import_module
from time import sleep

sys.path.append('lib')
sys.path.append('singleSleeve')
sys.path.append('multiSleeve')

from strip import Strip2D, getAddr

from PyQt5.QtCore import (
  Qt,
  QRect,
  QSize,
  QCoreApplication
)
from PyQt5.QtGui import (
  QIcon,
  QPixmap,
)

from PyQt5.QtWidgets import (
  QMainWindow,
  QApplication,
  QToolButton
)

def globalStop(self):
  print( "globalStop" )
  self.artnet.clear()
  self.send()

def stopAnimation():
  if globalInstance:
    globalInstance.quit = True
    if globalThread:
      # wait for the thread to finish
      print("Wait for the thread to end..")
      globalThread.join()

  strip2D.strip.clear()
  strip2D.strip.send()

strip2D = Strip2D(7, 21, addr = getAddr())
strip2D.strip.globalStop = globalStop

globalInstance = None
globalThread = None

def runLight(classDefinition):
  # TODO: get rid of global
  global globalInstance # pylint: disable=global-statement
  globalInstance = classDefinition(strip2D)
  globalInstance.run()
class Window(QMainWindow):
  def __init__(self, appWidth, appHeight):
    super().__init__()

    # setting title
    self.setWindowTitle("LED sleeve UI")

    # setting geometry
    self.setGeometry(100, 100, appWidth, appHeight)

    # calling method
    self.UiComponents()

    # showing all the widgets
    self.show()

  def resizeEvent(self, event):
    # print( "resized" )
    startX = 30
    startY = 30

    width = 140
    height = 180

    #print(event.size().width())
    appWidth = event.size().width()
    # appHeight = event.size().height()

    for button in self.findChildren(QToolButton):
      # print( f"{button.text()}: " )
      button.move(startX, startY)
      # print( button.text())
      startX += width + 5
      if startX + width + 30 > appWidth:
        startX = 30
        startY += height + 5

  # method for widgets
  def UiComponents(self):

    startX = 30
    startY = 30
    width = 140
    height = 180

    filenames = glob("singleSleeve/*.py")
    def addbutton( classInstance, classname, filename, x, y ):
      button = QToolButton(self)
      button.setText(classname)

      button.clicked.connect(self.bind(button,classInstance))
      # Find common image types to match the Class or module file
      files = []
      for file in (classname,  filename):
        for ext in ("svg", "png", "webp", "gif", "jpg", "jpeg"):
          files.extend( glob(f"resources/{file}.{ext}") )

      if files:
        rMyIcon = QPixmap(files[0])
        button.setIcon(QIcon(rMyIcon))
        button.setIconSize(QSize(130,130))
      button.setGeometry(QRect(x, y, width, height))
      button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

    # Add a stop button
    button = QToolButton(self)
    button.setText("STOP")
    button.clicked.connect( stopAnimation )
    # rMyIcon = QPixmap(files[0])
    # button.setIcon(QIcon(rMyIcon))
    # button.setIconSize(QSize(130,130))
    button.setGeometry(QRect(startX, startY, width, height))
    button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

    for filename in filenames:
      nameparts = re.split(r"/|\.py", filename)
      fancyName = nameparts[1].capitalize()

      try:
        print( f"loading {nameparts[1]}:", end="", flush=True )
        module = import_module(nameparts[1])

        # create 10 classnames, but omit the '0' suffix
        classNames = map( lambda n, fn=fancyName: n and f"{fn}{n}" or fn, range( 0,10 ))
        for classname in classNames:
          if hasattr(module, classname):
            print( f" {classname}", end="" )
            addbutton( getattr(module, classname ), classname, nameparts[1], startX, startY )
            startX += width + 5
            if startX + width + 30 > self.size().width():
              startX = 30
              startY += height + 5
        print( "" )

      except Exception as e: # pylint: disable=broad-except
        # Catch anything
        print( f"failed: {e}" )

    #self.showMaximized()

  def bind(self, button, classInstance):
    def boundFunction():
      button.setStyleSheet("color: red;")
      QCoreApplication.processEvents()

      # TODO: get rid of global
      global globalThread # pylint: disable=global-statement
      if globalInstance:
        globalInstance.quit = True
        if globalThread:
          # wait for the thread to finish
          print( "wait on previous thread to finish..")
          globalThread.join()

      for buttonx in self.findChildren(QToolButton):
        buttonx.setStyleSheet("color: white")

      # create a thread
      globalThread = thread = Thread(target=runLight, args=[classInstance])
      #thread = Thread(target=test)

      button.setStyleSheet("color: green;")
      #button.setStyleSheet("border : 2px solid black")
      button.setAutoFillBackground(True)
      button.setCheckable(True)
      button.setChecked(True)

      thread.start()

      #print( button.text() )
    return boundFunction

  # def selectFunction(self, button):
  #   print( button.text() )


fd = sys.stdin.fileno()
oldterm = termios.tcgetattr(fd)
newattr = termios.tcgetattr(fd)
newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
termios.tcsetattr(fd, termios.TCSANOW, newattr)

oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

# create pyqt5 app
app = QApplication(sys.argv)
#QString my_argv_0 = qApp->arguments().at(0);
#print( App.arguments()[1] )

screen = app.primaryScreen()
rect = screen.availableGeometry()

# create the instance of our Window
w, h = rect.width(), rect.height()
w,h=1400,820
window = Window( w, h )

# start the app
ret = app.exec()


stopAnimation()

termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

sys.exit(ret)
