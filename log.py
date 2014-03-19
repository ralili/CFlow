import logging
class log:
	def __init__(self):
		self.logger=logging.getLogger('myapp')
		self.formatter = logging.Formatter('%(message)s')
		self.hdlr = logging.FileHandler('/var/tmp/myapp.log')
		self.hdlr.setFormatter(formatter)
		self.logger.addHandler(hdlr) 
		self.logger.setLevel(logging.WARNING)

logger.error('We have a problem')