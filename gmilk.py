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

      self.menu = gtk.Menu()

      self.menuItem = gtk.ImageMenuItem(gtk.STOCK_QUIT)
      self.menuItem.connect('activate', self.quit, self.statusIcon)
      self.menu.append(self.menuItem)

      self.statusIcon.connect('popup-menu', self.popup_menu, self.menu)
      self.statusIcon.set_visible(1)
      gtk.main()

   def popup_menu(self, widget, button, time, data = None):
      if button == 3:
         data.show_all()
         data.popup(None, None, gtk.status_icon_position_menu, 3, time, self.statusIcon)

   def quit(self,widget,data=None):
      gtk.main_quit()

if __name__ == "__main__":
   gmilk = Gmilk()
