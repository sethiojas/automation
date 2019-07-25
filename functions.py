import subprocess
import webbrowser
from time import sleep
from functools import wraps
import yoda
import os

sleep_time = 300

def set_alert_msg(status_code):
	''' determine which message to send as email alert based on the status code '''

	# Task status 		code (int)
	
	#Command not in 	    random yoda quote  	
	#list
	
	# Started 				0
	
	# Ended 				1
	
	# Authentication 		2
	# failure

	#INCORRECT PATH 		3

	#PERMISSION ERROR		4

	alert_msg = ''

	if status_code == 0:
		alert_msg += 'Task Started'
	elif status_code == 1:
		alert_msg += 'Task Executed'
	elif status_code == 2:
		alert_msg += 'COMMAND CAN NOT BE EXECUTED: AUTHENTICATION FAILURE'
	elif status_code == 3:
		alert_msg += 'INCORRECT PATH : Path does not exists.'
	elif status_code == 4:
		alert_msg += 'PERMISSION ERROR : Path can not be executed'
	else:
		alert_msg = yoda.say_quote()

	return alert_msg



def execute_task(command, args, mail=None):
	''' Execute the task received in email '''

	#Task is executed based on the subject of email which is stored in command variable
	#of mail class. It is assumed that body of email is relevant as per the email Subject.
	#i.e. if command is browser then body contains only URLs seperated by newlines.
	#if command is exe then body contains path to script and commandline args(if required)

	if command.lower() == 'browser':
		for link in args:
			webbrowser.open(link)
			sleep(2)
	elif command.lower() == 'exe':
		exe_command(args, mail)
	elif command.lower() == 'sleep':
		change_sleep_time(args[0])
	else:
		if mail != None:
			mail.sent_mail = 1
			status_code = None
			mail.send_mail(status_code)


def exe_command(args, mail):
	''' Executes when command is 'exe' '''
	
	#Path of executable which is provided is checked for existence
	#if path exists then the program checks if it has execution rights 
	#for the executable. If both of the checks are passed then open_exe
	#function exeutes the program with command line args (optional)

	if os.path.exists(args[0]):
		if os.access(args[0], os.X_OK):
			open_exe(args)
		else:
			print('PERMISSION ERROR : Path can not be executed')
			mail.sent_mail = 1
			status_code = 4
			mail.send_mail(status_code)
	else:
		print('INCORRECT PATH : Path not found')
		mail.sent_mail = 1
		status_code = 3
		mail.send_mail(status_code)

def change_sleep_time(num):
	''' changes the amount of time system sleeps after checking one mail '''
	global sleep_time
	sleep_time = num

def get_sleep_time():
	''' return the amount of time to sleep after checking one mail '''
	global sleep_time
	return sleep_time

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