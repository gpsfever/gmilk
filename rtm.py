import sys
import locale
import gettext
import urllib
import hashlib 
import xml.dom.minidom

from task import *

RTM_API_KEY = "a4ab81f86a5276cf2145f92c8f74a486"
RTM_SHARED_SECRET = "7d068fd399131d9e"
RTM_SERVICE_METHODS = "http://www.rememberthemilk.com/services/rest/"
RTM_SERVICE_AUTH = "http://www.rememberthemilk.com/services/auth/"
RTM_HOME = "http://www.rememberthemilk.com/home/"

APP = "gmilk"
DIR = "locale"

class Rtm:
   def __init__(self,ui):
      self.ui = ui
      self.auth_token = ""

   def get_frob(self):
      try:
         args = {'method': 'rtm.auth.getFrob'}
         url = self.get_url(RTM_SERVICE_METHODS, args, False)
         rsp = self.get_response(url)
         return rsp.getElementsByTagName("frob")[0].childNodes[0].data
      except Exception as detail:
         sys.stderr.write("Error on get_frob: "+detail)

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

   def get_response(self, url):
      dom = xml.dom.minidom.parse(urllib.urlopen(url))
      rsp = dom.getElementsByTagName("rsp")[0]
      stat = rsp.getAttribute('stat')
      if stat == 'ok':
         return rsp
      else:
         self.raise_error(dom)

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
      frob = self.get_frob()
      args = {'perms': perms}
      return (self.get_url(RTM_SERVICE_AUTH, args, False, frob), frob)

   def get_task_list(self,filter=None):
      args = {'method': 'rtm.tasks.getList'}    
      if filter:
         args['filter'] = filter
      url = self.get_url(RTM_SERVICE_METHODS, args)
      rsp = self.get_response(url)
      tasks = []

      for taskseries_node in rsp.getElementsByTagName("taskseries"):
         id    = taskseries_node.getAttribute("id")
         name  = taskseries_node.getAttribute("name")
         tasks.append(Task(id,name))
      return tasks
