class Task:

   TODAY    = 0
   TOMORROW = 1
   DUE      = 2

   def __init__(self, type, id, name, due, list_id=None, series_id=None, menu_item=None):
      self.type      = type
      self.id        = id
      self.name      = name
      self.due       = due
      self.list_id   = list_id
      self.series_id = series_id
      self.menu_item = menu_item
