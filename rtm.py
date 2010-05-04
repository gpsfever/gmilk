import sys
import time
import locale
import gettext
import urllib
import hashlib 
import xml.dom.minidom

from task import *

RTM_API_KEY = "a4ab81f86a5276cf2145f92c8f74a486" # you can get yours at http://www.rememberthemilk.com/services/api/keys.rtm
RTM_SHARED_SECRET = "7d068fd399131d9e"
RTM_SERVICE_METHODS = "http://api.rememberthemilk.com/services/rest/"
RTM_SERVICE_AUTH = "http://www.rememberthemilk.com/services/auth/"
RTM_HOME = "http://www.rememberthemilk.com/home/"

APP = "gmilk"
DIR = "locale"

class Rtm:
   def __init__(self,ui):
      self.ui = ui
      self.auth_token = ""
      self.check = True

   def get_frob(self):
      try:
         args = {'method': 'rtm.auth.getFrob'}
         url = self.get_url(RTM_SERVICE_METHODS, args, False)
         rsp = self.get_response(url)
         return (rsp.getElementsByTagName("frob")[0].childNodes[0].data,None)
      except Exception as detail:
         sys.stderr.write("Error on get_frob: %s" % detail)
         return (None,detail.__str__())

   def get_auth_token(self, frob):
      args = {'method': 'rtm.auth.getToken'}
      url = self.get_url(RTM_SERVICE_METHODS, args, False, frob)
      rsp = self.get_response(url)
      return rsp.getElementsByTagName("token")[0].childNodes[0].data

   def set_auth_token(self,token):
      self.auth_token = token

   def check_token(self, token):
      if token==None or len(token)<1:
         return False

      args = {'method': 'rtm.auth.checkToken', 'auth_token': token}
      url = self.get_url(RTM_SERVICE_METHODS, args, False)

      try:
         rsp = self.get_response(url)
         info = {}
         info['token'] = rsp.getElementsByTagName("token")[0].childNodes[0].data
         info['perms'] = rsp.getElementsByTagName("perms")[0].childNodes[0].data
         user_node = rsp.getElementsByTagName("user")[0]
         info['user'] = {'id': user_node.getAttribute('id'),'username': user_node.getAttribute('username'),'fullname': user_node.getAttribute('fullname')}
         return info
      except Exception, msg:
         return False

   def get_url(self, base_url, args, with_auth_token=True, with_frob=None):
      try:
         args = self.sign_args(args, with_auth_token, with_frob)
      except Exception:
         sys.stderr.write("Error on get_url: "+detail)
      return base_url + '?' + urllib.urlencode(args)
    
   def sign_args(self, args, with_auth_token=True, with_frob=None):
      """
      @type args: dict
      @param with_auth_token: Whether the auth token should be appended
      @param with_frob: Optionally append given frob
      """
      try:
         if with_frob != None:
            args['frob'] = with_frob

         if with_auth_token:
            args['auth_token'] = self.auth_token

         args['api_key'] = RTM_API_KEY
         args['api_sig'] = self.get_signature(args)
      except Exception as detail:
         sys.stderr.write("Error on sign_args: "+detail)
      return args

   def connectivity(self):
      for i in range(10):
         print "Checking connectivity: %d" % i
         try:
            urllib.urlopen(RTM_HOME)
            print "Connected."
            return True
         except Exception as exc:
            print "Failed connectivity: %d %s" % (i,exc)
         time.sleep(5)
      return False

   def get_response(self, url):
      if self.check and not self.connectivity():
         raise Exception, "Failed to connect"
      self.check = False

      dom = xml.dom.minidom.parse(urllib.urlopen(url))
      rsp = dom.getElementsByTagName("rsp")[0]
      stat = rsp.getAttribute('stat')
      if stat == 'ok':
         return rsp
      else:
         self.raise_error(dom)
         self.check = True

   def get_signature(self, args):
      """
      Returns value of api_sig parameter
      @type args: dict
      """
      sig = RTM_SHARED_SECRET
      keys = args.keys()
      keys.sort()
      for key in keys:
         sig += key + str(args[key])
      return hashlib.md5(sig).hexdigest()

   def raise_error(self, dom):
      err = dom.getElementsByTagName('err')[0]
      code = err.getAttribute('code')
      msg = err.getAttribute('msg')
      raise Exception, "%s: %s" % (code, msg)

   def auth_url(self, perms):
      """
      Give this URL to the user that he can give permission to this application
      @param token: Can be read, write or delete
      """
      frob, msg = self.get_frob()
      if frob==None:
         return (None,None,msg)
      args = {'perms': perms}
      return (self.get_url(RTM_SERVICE_AUTH, args, False, frob), frob, msg)

   def create_timeline(self):
      args  = {'method': 'rtm.timelines.create'}    
      url   = self.get_url(RTM_SERVICE_METHODS, args)
      rsp   = self.get_response(url)
      time  = rsp.getElementsByTagName("timeline")
      if len(time)<1:
         return -1
      return time[0].firstChild.data

   def complete_task(self,task,timeline):
      args  = {'method': 'rtm.tasks.complete'}    
      args['timeline']        = timeline
      args['list_id']         = task.list_id
      args['taskseries_id']   = task.series_id
      args['task_id']         = task.id
      url   = self.get_url(RTM_SERVICE_METHODS, args)
      rsp   = self.get_response(url)
      ctask = rsp.getElementsByTagName("task");
      return len(ctask)>0

   def get_task_list(self,type,filter=None):
      args = {'method': 'rtm.tasks.getList'}    
      if filter:
         args['filter'] = filter
      url = self.get_url(RTM_SERVICE_METHODS, args)
      rsp = self.get_response(url)
      tasks = []

      for list_node in rsp.getElementsByTagName("list"):
          list_id = list_node.getAttribute("id")
          for taskseries_node in list_node.getElementsByTagName("taskseries"):
             sid  = taskseries_node.getAttribute("id")
             task = taskseries_node.getElementsByTagName("task")
             nts  = taskseries_node.getElementsByTagName("notes")
             ntg  = taskseries_node.getElementsByTagName("tags")
             id   = task[0].getAttribute("id")	if len(task)>0 else taskseries_node.getAttribute("id")
             due  = task[0].getAttribute("due") if len(task)>0 else taskseries_node.getAttribute("due")
             name = taskseries_node.getAttribute("name")

             note_str   = []
             notes      = nts[0].getElementsByTagName("note")
             for note in notes:
                note_str.append(note.firstChild.data)

             tags_str = []
             tags     = ntg[0].getElementsByTagName("tag")
             for tag in tags:
                tags_str.append(tag.firstChild.data)

             tasks.append(Task(type,id,name,due,list_id,sid,None,note_str,tags_str))
      return tasks
