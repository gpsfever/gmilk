#!/usr/bin/python
import locale
import gettext
import gtk
import pygtk
import gconf

pygtk.require('2.0')

from rtm import *
from task import *

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

      self.statusIcon.connect('popup-menu', self.popup_menu, self.menu)
      self.statusIcon.set_visible(1)
      self.init()

      self.menuItem = gtk.MenuItem(_("Authorize"))
      self.menuItem.connect('activate', self.authorize, self.statusIcon)
      self.menu.append(self.menuItem)

      self.menuItem = gtk.MenuItem(_("Quit"))
      self.menuItem.connect('activate', self.quit, self.statusIcon)
      self.menu.append(self.menuItem)
      gtk.main()

   def init(self):
      self.gconf	= gconf.client_get_default()
      self.frob	= self.gconf.get_string("/apps/gmilk/frob")
      self.token	= self.gconf.get_string("/apps/gmilk/token")
      self.rtm = Rtm(self)

      if self.rtm.check_token(self.token):
         self.rtm.set_auth_token(self.token)

         today_tasks    = self.rtm.get_task_list("due:today")
         tomorrow_tasks = self.rtm.get_task_list("due:tomorrow")
         due_tasks      = self.rtm.get_task_list("dueBefore:today NOT completedBefore:today")

         self.add_tasks(_("Today tasks"),today_tasks)
         self.add_tasks(_("Tomorrow tasks"),tomorrow_tasks)
         self.add_tasks(_("Due tasks"),due_tasks)

   def add_tasks(self,title,tasks):
      self.menuItem = gtk.MenuItem(title)
      self.menu.append(self.menuItem)

      for task in tasks:
         self.menuItem = gtk.MenuItem(task.name)
         self.menuItem.connect('activate', self.quit, self.statusIcon)
         self.menu.append(self.menuItem)

      self.menu.append(gtk.SeparatorMenuItem())

   def popup_menu(self, widget, button, time, data = None):
      if button == 3:
         data.show_all()
         data.popup(None, None, gtk.status_icon_position_menu, 3, time, self.statusIcon)

   def quit(self,widget,data=None):
      gtk.main_quit()

   def show_error(self,msg):
		self.show_dialog(gtk.MESSAGE_ERROR,msg)

   def show_info(self,msg):
		self.show_dialog(gtk.MESSAGE_INFO,msg)

   def show_dialog(self,msg_type,msg):		
		dialog = gtk.MessageDialog(None,gtk.DIALOG_MODAL,msg_type,gtk.BUTTONS_OK,msg)
		dialog.run()
		dialog.destroy()

   def authorize(self,widget,data=None):
		(url,frob) = self.rtm.auth_url("delete")

		self.gconf.set_string("/apps/gmilk/frob",frob)

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

		if self.rtm.check_token(token):
			self.show_info(_("Authorized! You should now be able to use this app now."))
			self.gconf.set_string("/apps/gmilk/token",token)
		else:
			self.show_error(_("Invalid authorization, please try again."))

if __name__ == "__main__":
   gmilk = Gmilk()
