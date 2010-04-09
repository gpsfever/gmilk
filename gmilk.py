#!/usr/bin/python
__appname__    = "Gmilk"
__author__     = "Eustaquio 'TaQ' Rangel"
__copyright__  = "2010 Eustaquio 'TaQ' Rangel"
__version__    = "0.0.1"
__license__    = "GPL"
__email__      = "eustaquiorangel@gmail.com"
__website__    = "http://github.com/taq/gmilk"
__date__       = "$Date: 2010/04/08 12:00:00$"

import threading
import locale
import gettext
import gtk
import gobject
import pygtk
import gconf

pygtk.require('2.0')

from rtm import *
from task import *

gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)
_ = gettext.gettext

gobject.threads_init()

class InitThread(threading.Thread):
   def __init__(self,gui):
      super(InitThread,self).__init__()
      self.gui = gui

   def run(self):
      self.gui.init()

class Gmilk:

   def __init__(self):
      self.menu = gtk.Menu()

      self.statusIcon = gtk.StatusIcon()
      self.statusIcon.set_from_file("./images/empty.png")
      self.statusIcon.set_visible(True)
      self.statusIcon.set_tooltip("Remember the milk")
      self.statusIcon.connect('activate'  , self.left_click , self.menu)
      self.statusIcon.connect('popup-menu', self.right_click, self.menu)
      self.statusIcon.set_tooltip(_("Asking the task list to Remember the Milk ..."))
      self.statusIcon.set_visible(1)

      t = InitThread(self)
      t.start()
      gtk.main()

   def init(self):
      self.gconf  = gconf.client_get_default()
      self.frob   = self.gconf.get_string("/apps/gmilk/frob")
      self.token  = self.gconf.get_string("/apps/gmilk/token")
      self.rtm    = Rtm(self)

      if self.rtm.check_token(self.token):
         self.rtm.set_auth_token(self.token)
         self.check_tasks()
      else:
         self.make_authorize_menuitem()

   def clear_menu(self):
      for menuitem in self.menu.get_children():
         self.menu.remove(menuitem)

   def make_authorize_menuitem(self):
      self.authorizeItem = gtk.MenuItem(_("Authorize"))
      self.authorizeItem.connect('activate', self.authorize, self.statusIcon)
      self.menu.append(self.authorizeItem)
      self.statusIcon.set_tooltip(_("Need to authorize. Click on 'Authorize' on the menu."))
      self.blinking(True)

      self.make_about_menuitem()
      self.make_quit_menuitem()

   def remove_authorize_menuitem(self):
      if self.authorizeItem!=None:
         self.menu.remove(self.authorizeItem)

   def make_about_menuitem(self):
      self.aboutItem = gtk.MenuItem(_("About"))
      self.aboutItem.connect('activate', self.about, self.statusIcon)
      self.menu.append(self.aboutItem)

   def make_quit_menuitem(self):
      self.quitItem = gtk.MenuItem(_("Quit"))
      self.quitItem.connect('activate', self.quit, self.statusIcon)
      self.menu.append(self.quitItem)

   def check_tasks(self):
      self.statusIcon.set_tooltip(_("Checking your tasks ..."))

      today_tasks    = self.rtm.get_task_list("due:today")
      tomorrow_tasks = self.rtm.get_task_list("due:tomorrow")
      due_tasks      = self.rtm.get_task_list("dueBefore:today NOT (completedBefore:today or completed:today)")

      self.clear_menu()
      self.add_tasks(_("No tasks today")    if len(today_tasks)<1    else _("Today tasks"),today_tasks)
      self.add_tasks(_("No tasks tomorrow") if len(tomorrow_tasks)<1 else _("Tomorrow tasks"),tomorrow_tasks)
      self.add_tasks(_("No due tasks")      if len(due_tasks)<1      else _("Due tasks"),due_tasks)
      self.tasks_alert(len(today_tasks),len(tomorrow_tasks),len(due_tasks))

      self.make_about_menuitem()
      self.make_quit_menuitem()

   def tasks_alert(self,today,tomorrow,due):
      self.statusIcon.set_tooltip(_("%s tasks found.") % (today+tomorrow+due))
      if due>0:
         self.statusIcon.set_from_file("./images/due.png")
      elif today>0:
         self.statusIcon.set_from_file("./images/today.png")
      elif tomorrow>0:
         self.statusIcon.set_from_file("./images/tomorrow.png")
      else:
         self.statusIcon.set_from_file("./images/empty.png")
      self.blinking(True)

   def blinking(self,blink):
      self.statusIcon.set_blinking(blink)

   def add_tasks(self,title,tasks):
      self.menuItem = gtk.MenuItem(title)
      self.menu.append(self.menuItem)

      for task in tasks:
         self.menuItem = gtk.MenuItem("- "+task.name)
         self.menuItem.connect('activate', self.quit, self.statusIcon)
         self.menu.append(self.menuItem)

      self.menu.append(gtk.SeparatorMenuItem())

   def right_click(self, widget, button, time, data = None):
      self.blinking(False)
      self.show_menu(widget,button,time,data)

   def left_click(self,widget,data):
      self.blinking(False)
      self.show_menu(widget,0,gtk.get_current_event_time(),data)

   def show_menu(self,widget,button,time,data):
      data.show_all()
      data.popup(None, None, gtk.status_icon_position_menu, button, time, self.statusIcon)

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

      label    = gtk.Label(_("Please enter the following URL on your browser"))
      text     = gtk.Entry()
      dialog   = gtk.Dialog(_("Asking authorization"),None,gtk.DIALOG_MODAL,(gtk.STOCK_OK, gtk.RESPONSE_ACCEPT, gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))

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
         self.remove_authorize_menuitem()
         self.rtm.set_auth_token(token)
         self.show_info(_("Authorized! You should now be able to use this app now."))
         self.gconf.set_string("/apps/gmilk/token",token)
         self.check_tasks()
      else:
         self.show_error(_("Invalid authorization, please try again."))

   def about(self,widget,data=None):
      self.about = gtk.AboutDialog()
      self.about.set_name(__appname__)
      self.about.set_program_name(__appname__)
      self.about.set_version(__version__)
      self.about.set_copyright(__copyright__)
      self.about.set_license(__license__)
      self.about.set_website(__website__)
      self.about.set_website_label(__website__)
      self.about.set_authors(["%s <%s>" % (__author__,__email__)])
      self.about.show()

if __name__ == "__main__":
   gmilk = Gmilk()
