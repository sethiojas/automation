#---------------------------USAGE----------------------------------------------------------
#VALID SUBJECTS :
#1)browser 
#2)exe
#<subjects are case insensitive>

#subject: (One of the given valid entires)
#<body>
#link or path/to/executable
#command --
#line     |
#args     |-------> only if subject is exe
#for	  |
#script----

#---------------------------------------------------------------------------------------------
from time import sleep
from os import system
from mail_func import Mail
import functions

#-----------------------------TO BE FILLED--------------------------------------------------

#bot id and password
#gmail id required
#if any other id is to be used then change the search function of IMAP
bot_id = 'bruhbotman@gmail.com'
bot_passwd = '1q2w3e!@'

#Mail id to receive email alerts on
receiver_id = 'ojas.sethi@outlook.com'

#instructions sent from only this email will be executed
allowed_email = 'ojas.sethi@outlook.com'
sender_name = 'Ojas' #Name of account Holder of the above give allowed_id

mail = Mail(bot_id, bot_passwd, receiver_id, allowed_email, sender_name)


#--------------------------------------------------------------------------------------------

try:
	while True:
		
		system('clear')
		print('Logging In....')

		task_msg = mail.read_mail()

		if task_msg != False:

			command = task_msg['command']
			text_msg = task_msg['text_msg']

			#list of arguments
			#remove space characters from left and right of string
			#then split on space characters in between
			args = text_msg.strip().split()

			#send email alert that task has started
			status_code = 0
			print("Task Status : START")
			mail.send_mail(status_code)

			#Execute task
			functions.execute_task(command, args, mail)

			#send email alert that task has ended
			status_code = 1
			print("Task Status : ENDED")
			mail.send_mail(status_code)

		else:
			print("Authentication Failure")
			status_code = 2
			mail.send_mail(status_code)

		sleep(5)
		system('clear')
		print('Sleeping....')
		
		#sleep for 5 minutes before checking email again
		sleep(300)

#stop if keyboard interrupt is encountered
except KeyboardInterrupt:
	print('\nStoping...')
	sleep(0.5)