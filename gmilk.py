#!/usr/bin/python
import pygtk
pygtk.require('2.0')
import gtk

class Gmilk:

  def __init__(self):
    self.statusIcon = gtk.StatusIcon()
    self.statusIcon.set_from_file("./images/rememberthemilk.png")
    self.statusIcon.set_visible(True)
    self.statusIcon.set_tooltip("Remember the milk")
    gtk.main()

if __name__ == "__main__":
  gmilk = Gmilk()
