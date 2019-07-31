import threading
import pexpect
import Queue
import re
import time

class cxn():
	SSH_NEWKEY = r'Are you.*?\?'
	EN_PROMPT = r'([#>\$]) ?$'
	ERR_PROMPT = r'\^'
	WORKERS = 2
	LOGS = ''
	
	def __init__(self, username, password):
		self.time = { 'start': time.time(), 'end': '' }
		self.queue = Queue.Queue()
		self.username = username
		self.password = password

	def start(self):
		for i in range(self.WORKERS):
			self.thread = threading.Thread(target=self.worker) 
			self.thread.daemon = True
			self.thread.start()

		self.queue.join()
		self.time['end'] = time.time()
		return
		
	def add(self, hostname):
		self.queue.put(hostname)

	def login(self, hostname, logging=True):
		try:
			child = pexpect.spawn('ssh -l %s %s'%(self.username, hostname))

			if logging:
				child.logfile_read = file('{}/{}.txt'.format(LOGS, str(hostname)), 'a+')

			options = [
				self.EN_PROMPT, 
				self.SSH_NEWKEY, 
				'[Pp]assword:\s+', 
				'Permission denied', 
				'Authentication failed.', 
				pexpect.EOF, 
				pexpect.TIMEOUT, 
				'not resolve'
			]

			i = child.expect(options)
			while True:
				if i == 0:
					return child
				elif i == 1:
					child.sendline('yes')
				elif i == 2:
					child.sendline(self.password)
				else:
					child.terminate()
					print("THERE WAS AN ERROR")
					return None

				i = child.expect(options)
		
		except Exception as e:
			print(e)

	def worker(self):
		while True:
			hostname = self.queue.get()
			child = True 
			#child = self.login(hostname)
			if child:
				print(hostname)
				#child.close()
			self.queue.task_done()

