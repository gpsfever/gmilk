#!/usr/bin/python
import locale
import gettext
import gtk
import pygtk

pygtk.require('2.0')

from rtm import *

gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)
_ = gettext.gettext

class Gmilk:

   def __init__(self):
      self.statusIcon = gtk.StatusIcon()
      self.statusIcon.set_from_file("./images/rememberthemilk.png")
      self.statusIcon.set_visible(True)
      self.statusIcon.set_tooltip("Remember the milk")

      self.menu = gtk.Menu()

      self.menuItem = gtk.MenuItem(_("Authorize"))
      self.menuItem.connect('activate', self.authorize, self.statusIcon)
      self.menu.append(self.menuItem)

      self.menuItem = gtk.MenuItem(_("Quit"))
      self.menuItem.connect('activate', self.quit, self.statusIcon)
      self.menu.append(self.menuItem)

      self.statusIcon.connect('popup-menu', self.popup_menu, self.menu)
      self.statusIcon.set_visible(1)
      self.init()
      gtk.main()

   def init(self):
      rtm = Rtm(self)

   def popup_menu(self, widget, button, time, data = None):
      if button == 3:
         data.show_all()
         data.popup(None, None, gtk.status_icon_position_menu, 3, time, self.statusIcon)

   def quit(self,widget,data=None):
      gtk.main_quit()

   def authorize(self,widget,data=None):
      pass

   def auth_dialog(self):
      print "estou no dialogo"
      dialog = gtk.Dialog(_("Asking authorization"),None,0,(_("Ask"),_("Cancel")))
      dialog.show()

if __name__ == "__main__":
   gmilk = Gmilk()
