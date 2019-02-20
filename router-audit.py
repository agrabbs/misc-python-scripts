import threading
import getpass
import pexpect
import base64
import Queue
import csv
import re
import time
import sys

######### CONFIGURATION #########
SSH_NEWKEY = r'Are you.*?\?'
USER_PROMPT = '>$'
EN_PROMPT = '([#>]) ?$'
HOSTNAMES = list()
MAX_THREADS = 200
LOG_DIR = 'logs/'
####### END CONFIGURATION #######

username = raw_input("Username: ")
password = getpass.getpass()

with open('example.csv') as csvfile:
	reader = csv.reader(csvfile)
	for row in reader:
		HOSTNAMES.append((row[0]))


def login(hostname, logging='on'):
	hostname = hostname
	logging = logging
	try:
		child = pexpect.spawn('ssh -l %s %s'%(username, hostname))

		if logging == 'on':
			fout = file('{}/childlog_{}.txt'.format(LOG_DIR, str(hostname), 'w')
			child.logfile_read = fout
		
		i = child.expect([SSH_NEWKEY, '[Pp]assword:\s+', pexpect.EOF])
		if i == 0:
			child.sendline('yes')
			child.expect('[Pp]assword: ')	
			child.sendline(password)
			child.expect(EN_PROMPT)
			child.sendline("!")
			child.expect(EN_PROMPT)
			return child
		elif i == 1:
			child.sendline(password)
			child.expect(EN_PROMPT)
			child.sendline('!')
			child.expect(EN_PROMPT)
			return child
		elif i == 2:
			print("{},ERROR, NO CONNECTION".format(hostname))
			child.terminate()
			return None

	except pexpect.TIMEOUT:
		print("{}, ERROR, TIMEOUT".format(hostname))


def worker():
	while True:
		host = queue.get()
		child = login(host)
		if child:
			child.sendline('term len 0')
			child.expect(EN_PROMPT)
			child.sendline('show bgp neighbor-group TEST-GROUP configuration | inc maximum | utility wc lines')
			child.expect(EN_PROMPT)

			search = re.search(r'\s(\d)\s',child.before)
			if search:
				edge = search.group(0).strip()
			else:
				edge = 'Not Found'
			if edge != '3':
				child.sendline('show bgp neighbor-group ?')
				child.expect(EN_PROMPT)
				search = re.search(r'TEST-GROUP-BUG', child.before)
				if search:
					edge = search.group(0)
				else:
					edge = 'No TEST-GROUP Configured'
					child.sendline('show bgp neighbor-group TEST-GROUP configuration')
					child.expect(EN_PROMPT)
					print(child.before)

			print('{}: {}'.format(host, edge))
			child.sendline('logout')
			child.close()
		queue.task_done()
	

if __name__ == "__main__":
	start = time.time()
	queue = Queue.Queue()

	for HOST in HOSTNAMES:
		queue.put(HOST)

	for i in range(MAX_THREADS):
		thread = threading.Thread(target=worker) 
		thread.daemon = True
		thread.start()

	print '*** Waiting for Workers'
	queue.join()
	print '*** Done'
	end = time.time()
	print end - start
