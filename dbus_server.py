import dbus, dbus.glib, dbus.service

class DbusServer(dbus.service.Object):
   def set_manager(self,manager):
      self.manager = manager

   @dbus.service.method(dbus_interface="com.Gmilk.Interface",in_signature="",out_signature="i")
   def task_count(self):
      return self.manager.task_count()
