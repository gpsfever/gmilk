class Task:
   def __init__(self, id, name, due, list_id=None, series_id=None):
      self.id			= id
      self.name		= name
      self.due			= due
      self.list_id	= list_id
      self.series_id	= series_id
