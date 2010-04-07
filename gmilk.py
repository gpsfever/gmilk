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
      self.rtm = Rtm(self)

   def popup_menu(self, widget, button, time, data = None):
      if button == 3:
         data.show_all()
         data.popup(None, None, gtk.status_icon_position_menu, 3, time, self.statusIcon)

   def quit(self,widget,data=None):
      gtk.main_quit()

   def show_error(self,msg):
		self.show_dialog(gtk.MESSAGE_ERROR)

   def show_error(self,msg):
		self.show_dialog(gtk.MESSAGE_INFO)

   def show_dialog(msg_type):		
		dialog = gtk.MessageDialog(None,gtk.DIALOG_MODAL,msg_type,gtk.BUTTONS_OK,msg)
		dialog.run()
		dialog.destroy()

   def authorize(self,widget,data=None):
		(url,frob) = self.rtm.auth_url("delete")
		label		= gtk.Label(_("Please enter the following URL on your browser"))
		text		= gtk.Entry()
		dialog	= gtk.Dialog(_("Asking authorization"),None,gtk.DIALOG_MODAL,(gtk.STOCK_OK, gtk.RESPONSE_ACCEPT, gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))

		text.set_text(url)
		text.set_editable(False)

		dialog.vbox.pack_start(label)
		dialog.vbox.pack_start(text)
		label.show()
		text.show()
		response = dialog.run()
		dialog.destroy()

		if response==gtk.RESPONSE_REJECT:
			self.show_error(_("You need authorization to use this app"))
			return

		try:
			token = self.rtm.get_auth_token(frob)
		except Exception as detail:
			self.show_error(_("Did you give authorization to this app? Please try again."))
			return

		print "token:"
		print token
		if self.rtm.check_token(token):
			self.show_info(_("You should now be able to use this app now."))
		else:
			self.show_error(_("Invalid authorization, please try again."))

if __name__ == "__main__":
   gmilk = Gmilk()
