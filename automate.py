from time import sleep
from os import system
from mail_func import Mail
import functions

#Get required data to initialize Mail object
data = functions.decrypt_and_parse_data()
try:
	# If data is empty then raise Interrupt, otherwise proceed normally
	if not data:
		raise KeyboardInterrupt

	mail = Mail(
		data['bot_id'], data['bot_passwd'], data['receiver_id'],
		data['allowed_email'], data['sender_name'], data['download_path']
		)

	while True:
		
		system('clear')
		print('Logging In....')

		task_msg = mail.read_mail()

		#task_msg is False if no mail is received. 
		if not task_msg:
			print('No Mail Found')
			functions.clrscr_and_pause()
			continue

		#task_msg has value 'fail' if the sender's email is not
		#authorized to send commands
		if task_msg == 'fail':
			print("Email Authentication Failure")
			status_code = 2
			mail.send_mail(status_code)
			functions.clrscr_and_pause()
			continue

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
			status_code = 1
			print("Task Status : ENDED")
			mail.send_mail(status_code)
		
		#Reset sent_mail to indicate Zero mails sent.
		mail.sent_mail = 0 
			
		functions.clrscr_and_pause()

#stop if keyboard interrupt is encountered
except KeyboardInterrupt:
	print('\nStopping...')
	sleep(0.5)