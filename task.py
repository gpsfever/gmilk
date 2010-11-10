class Task:

   TODAY    = 0
   TOMORROW = 1
   DUE      = 2
   TAGGED   = 3

   def __init__(self, type, id, name, due, list_id=None, series_id=None, menu_item=None, notes=None, tags=None, url=None):
      self.type      = type
      self.id        = id
      self.name      = name
      self.due       = due
      self.list_id   = list_id
      self.series_id = series_id
      self.menu_item = menu_item
      self.notes     = notes
      self.tags      = tags
      self.url       = url

   def __str__(self):
      return "%s %s %s %s %s %s" % (self.type,self.id,self.name,self.due,",".join(self.tags),self.url)
