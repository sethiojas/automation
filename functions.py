import subprocess
import webbrowser
from time import sleep
from functools import wraps
import yoda
import os


def set_alert_msg(status_code):
	''' determine which message to send as email alert based on the status code '''

	# Task status 		code (int)
	
	#Command not in 	   -1  	
	#list
	
	# Started 				0
	
	# Ended 				1
	
	# Authentication 		2
	# failure

	#INCORRECT PATH 		3

	#PERMISSION ERROR		4


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

	elif status_code == 3:
		alert_msg += 'INCORRECT PATH : Path not found'

	elif status_code == 4:
		alert_msg += 'PERMISSION ERROR : Path can not be executed'

	else:
		alert_msg = yoda.say_quote()

	return alert_msg



def execute_task(command, args, mail=None):
	''' Execute the task received in email '''

	#if command is browser then fetch link and open it in default browser
	if command.lower() == 'browser':
		#assuming all arguments are links if subject is browser
		#open all links
		for link in args:
			webbrowser.open(link)
			sleep(2)

	#if command matches exe then run executable (optional : command line args)
	elif command.lower() == 'exe':
		if os.path.exists(args[0]):
			if os.access(args[0], os.X_OK):
				open_exe(args)
			else:
				print('PERMISSION ERROR : Path can not be executed')
				status_code = 4
				mail.sendmail(status_code)
		else:
			print('INCORRECT PATH : Path not found')
			status_code = 3
			mail.sendmail(status_code)

	else:
		if mail != None:
			status_code = -1
			mail.sendmail(status_code)


#helps to implement the optional command line arguments functionality
#of open_exe() function
def wrapper_to_open_exe(open_exe):
	@wraps(open_exe)
	def inner(args):
		if len(args) > 1:
			command_line_args = ' '.join(args[1:])
		else:
			command_line_args = None

		open_exe(args, command_line_args)

	return inner

@wrapper_to_open_exe
def open_exe(args, command_line_args = None):
	''' open executables (Optional : command line arguments) '''
	if command_line_args:
		task = subprocess.Popen([args[0], command_line_args])
		task.wait()
	else:
		task = subprocess.Popen(args[0])
		task.wait()

if __name__ == '__main__':
	main()