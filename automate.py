from time import sleep
from os import system
from mail_func import Mail
import functions

#-----------------------------TO BE FILLED--------------------------------------------------

#bot id and password
#gmail id required
#if any other id is to be used then change the search function of IMAP
bot_id = ''
bot_passwd = ''

#Mail id to receive email alerts on
receiver_id = ''

#instructions sent from only this email will be executed
allowed_email = []
sender_name = '' #Name of account Holder of the above give allowed_id

#attachments (.txt files) in email get downloaded to this directory
#eg /home/manjaro/Downloads/email 
download_path = ''

mail = Mail(bot_id, bot_passwd, receiver_id, allowed_email, sender_name, download_path)

#--------------------------------------------------------------------------------------------

try:
	while True:
		
		system('clear')
		print('Logging In....')

		task_msg = mail.read_mail()

		if task_msg != False:

			if task_msg == 'fail':
				print("Authentication Failure")
				status_code = 2
				mail.send_mail(status_code)
			
			else:
				
				command = task_msg['command']
				text_msg = task_msg['text_msg']
				
				args = text_msg.strip().split()

				#send email alert that task has started
				status_code = 0
				print("Task Status : START")
				mail.send_mail(status_code)

				#Execute task
				functions.execute_task(command, args, mail)

				#check if a mail other than Task Started alert has been sent
				if mail.sent_mail == 0:
					#send email alert that task has ended
					status_code = 1
					print("Task Status : ENDED")
					mail.send_mail(status_code)
				else:
					mail.sent_mail = 0 #set sent_mail to 0 before other task
		else:
			print('No Mail Found')

		sleep(5)
		system('clear')
		print('Sleeping....')
		
		#sleep for specified amount of time (Defaults to 5 minutes)
		#before checking email again
		t = functions.get_sleep_time()
		print(f'Sleeping for {t} seconds')
		sleep(t)

#stop if keyboard interrupt is encountered
except KeyboardInterrupt:
	print('\nStoping...')
	sleep(0.5)