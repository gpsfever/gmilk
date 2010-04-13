import dbus, dbus.glib, dbus.service

class DbusServer(dbus.service.Object):
   def set_manager(self,manager):
      self.manager = manager

   @dbus.service.method(dbus_interface="com.Gmilk.Interface",in_signature="",out_signature="i")
   def task_count(self):
      return self.manager.task_count()

   @dbus.service.method(dbus_interface="com.Gmilk.Interface",in_signature="",out_signature="sss")
   def get_task(self,pos):
      return self.manager.get_task(pos)

   @dbus.service.method(dbus_interface="com.Gmilk.Interface",in_signature="",out_signature="b")
   def complete_task(self,id):
      task = self.manager.find_task_by_id(id)
      if task==None:
         return False
      return self.manager.complete(None,task)
