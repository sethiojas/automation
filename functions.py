import subprocess
import webbrowser
from time import sleep


def set_alert_msg(status_code):
	''' determine which message to send as email alert based on the status code '''

	# Task status 		code (int)
	
	# Started 				0
	
	# Ended 				1
	
	# Authentication 		2
	# failure

	alert_msg = 'Subject: TASK STATUS\n'

	#task started email
	if status_code == 0:
		alert_msg += 'Started'
	
	#task ended email
	elif status_code == 1:
		alert_msg += 'Executed'
	
	#if email is not from allowed email address
	elif status_code == 2:
		alert_msg += 'COMMAND CAN NOT BE EXECUTED: AUTHENTICATION FAILURE'

	return alert_msg



def execute_task(command, args):
	''' Execute the task received in email '''

	#if command is browser then fetch link and open it in default browser
	if command.lower() == 'browser':
		#assuming all arguments are links if subject is browser
		#open all links
		for link in args:
			webbrowser.open(link)
			sleep(2)
		
	#if command matches open then open the given executable
	elif command.lower() == 'open':
		
		task = subprocess.Popen(args[0])
		task.wait()

	#if command matches exe then run executable with command line args
	elif command.lower() == 'exe':

		command_line_args = ' '.join(args[1:])
		task = subprocess.Popen([args[0], command_line_args])
		task.wait()

if __name__ == '__main__':
	main()