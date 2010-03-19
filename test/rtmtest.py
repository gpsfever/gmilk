import unittest
import sys
import re
from rtm import *

sys.path.append("../")

class RtmTest(unittest.TestCase):
	def setUp(self):
		self.rtm = Rtm()
	
	def testFrob(self):
		frob = self.rtm.get_frob()
		assert re.search("^[0-9a-zA-Z]{40}$",frob) is not None

if __name__ == "__main__":
	unittest.main()   		
