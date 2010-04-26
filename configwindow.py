import gtk
import pygtk
import gettext

_ = gettext.gettext

class ConfigWindow(gtk.Window):
   def __init__(self,manager):
      super(ConfigWindow,self).__init__()
      self.set_title(_("Gmilk configuration"))
      self.set_modal(True)
   
      self.manager      = manager
      self.gconf        = self.manager.gconf
      self.resp         = None
      table             = gtk.Table(2,2,True)

      intervalStr         = gtk.Label(_("Interval (minutes)"))
      self.intervalTxt    = gtk.Entry()
      self.intervalTxt.set_text(str(self.manager.interval))

      self.ok  = gtk.Button(_("Ok"))
      self.ok.connect("clicked",self.save)

      self.cancel = gtk.Button(_("Cancel"))
      self.cancel.connect("clicked",self.dontsave)

      table.attach(intervalStr,0,1,1,2)
      table.attach(self.intervalTxt,1,2,1,2)

      table.attach(self.ok,0,1,3,4)
      table.attach(self.cancel,1,2,3,4)
      
      self.add(table)
      self.show_all()

   def save(self,widget):
      interval = int(self.intervalTxt.get_text())
      self.manager.gconf.set_int("/apps/gmilk/interval",interval)
      self.manager.interval = interval

      self.destroy()

   def dontsave(self,widget):
      self.destroy()
