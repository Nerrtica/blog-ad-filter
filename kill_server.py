'''
	kill flask server process
'''
import signal
import os

with open('process.txt') as f:
	s = f.read()

process_list = s.split('\n')

process_id = []
for process in process_list:
	if 'BlogAdFilter' in process or 'in_check' in process:
		process_id.append(process.split()[0])

for i in process_id:
	os.kill(int(i), signal.SIGKILL)
