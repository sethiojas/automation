#!/usr/bin/python3

#VALID SUBJECTS :
#('Browser, browser, BROWSER')
#('open', 'Open', 'OPEN')
#('exe', 'Exe', 'EXE')


#subject: (One of the given valid entires)
#body
#---------leave first line of body -------------------
#link|path/to/executable
#command --
#line     |
#args     |-------> only if subject is exe
#for	  |
#script----

from time import sleep
import imapclient
import pyzmail
import smtplib
from bs4 import BeautifulSoup
import subprocess
import threading
import webbrowser
from os import system

#-----------------------------TO BE FILLED--------------------------------------------------

#bot id and password
#gmail id required
#if any other id is to be used then change the search function of IMAP
bot_id = ''
bot_passwd = ''

#ID to receive task status on
receiver_id = ''

#instructions sent from only this email will be executed
allowed_email = ''
sender_name = '' #sender name of allowed id 

#--------------------------------------------------------------------------------------------

#function to mail task status
def send_mail(status, msg):
	#login into bot account
	mail = smtplib.SMTP('smtp.gmail.com', 587)
	mail.ehlo()
	mail.starttls()
	mail.login(bot_id, bot_passwd)

	#task started email
	if status == 0:
		mail.sendmail(bot_id, receiver_id,
			'Subject: TASK STATUS\nStarted')
	#task ended email
	elif status == 1:
		mail.sendmail(bot_id, receiver_id,
			'Subject: TASK STATUS\nExecuted')
	#if email is not from allowed email address
	elif status == 3:
		mail.sendmail(bot_id, receiver_id,
			'Subject: TASK STATUS\nCOMMAND CAN NOT BE EXECUTED: AUTHENTICATION FAILURE')
	#logout from bot id
	mail.quit()

	#display in command line which mail is sent
	#Task started or Task Ended
	print(msg)


try:
	while True:
		#To keep an eye on threads
		active_threads = []
		
		system('clear')
		print('Logging In....')
		
		#login to bot email
		email_read = imapclient.IMAPClient('imap.gmail.com', ssl=True)
		email_read.login(bot_id, bot_passwd)
		email_read.select_folder('INBOX', readonly = False)

		#search email by allowed sender name
		uid = email_read.gmail_search(sender_name)
		
		if uid: #if mail found
			print('Mail found')
			
			#get mail body
			raw = email_read.fetch(uid,'BODY[]')
			msg = pyzmail.PyzMessage.factory(raw[uid[0]][b'BODY[]'])
			
			#check if email address matches the allowed email
			if msg.get_addresses('from')[0][1] == allowed_email
				command = msg.get_subject() #if true then command equals subject of email
			else:
				command = None #if not true then command has None value
			
			#get html form of mssg body
			text = msg.html_part.get_payload().decode()
		 	
		 	#delete the just read email forever
			email_read.delete_messages(uid[0])
			email_read.expunge()
			
			#logout from email
			email_read.logout()

			#if command is not None
			if command:
				print("Task Status : START")
				thread_mail = threading.Thread(target = send_mail, args = [0, 'Mail Sent : START status'])
				active_threads.append(thread_mail)
				thread_mail.start()
			
				#parse html form of mssg body
				soup = BeautifulSoup(text, 'html.parser')
				
				#if command is browser then fetch link and open it in default browser
				if command in ('Browser, browser, BROWSER'):
					link_temp = soup.findAll('div',dir='auto')[1] #in second div tag (first div tag is white spaces)
					link = link_temp.find('a')['href'] # href value of anchor tag inside second div tag
					
					webbrowser.open(link)
					sleep(2)
					
				# ['\r\n',----------------------------------------------------------------------redundant
				#	'\n\nDips and nachos\nPasta sauce\nSpaghetti\nLasagna\nNoodles\n\n', -------redundant
				#  '\nDips and nachos\nPasta sauce\nSpaghetti\nLasagna\nNoodles\n', ------------redundant
				#  'Dips and nachos',
				#  'Pasta sauce',
				#  'Spaghetti',
				#  'Lasagna',
				#  'Noodles']

				#if command matches open then open the given executable
				elif command in ('open', 'Open', 'OPEN'):
					args = [member.get_text() for member in soup.findAll('div', dir='auto') if member.get_text() 
					not in ('\n','\r','\r\n') and not member.get_text().startswith('\n')]
					
					task = subprocess.Popen(args[0])
					task.wait()

				#if command matches exe then run executable with command line args
				elif command in ('exe', 'Exe', 'EXE'):
					args = [member.get_text() for member in soup.findAll('div', dir='auto') if member.get_text() 
					not in ('\n','\r','\r\n') and not member.get_text().startswith('\n')]
					
					command_line_args = ' '.join(args[1:])
					task = subprocess.Popen([args[0], command_line_args])
					task.wait()

				
				print("Task Status : ENDED")
				thread_mail = threading.Thread(target = send_mail, args = [1, 'Mail sent : ENDED status'])
				active_threads.append(thread_mail)
				thread_mail.start()
			
			#email was not from allowed email and command was set to None as a result of it
			else:
				error_msg = 'COMMAND CAN NOT BE EXECUTED: AUTHENTICATION FAILURE'
				print(error_msg)
				send_mail(3, error_msg)

		#If no mail is found by the name of sender
		else:
			print('No mail found')
		
		#wait for threads to complete (if any)
		for threads in active_threads:
			threads.join()
		
		sleep(5)
		system('clear')
		print('Sleeping....')
		
		#sleep for 5 minutes before checking email again
		sleep(300)
#stop if keyboard interrupt is encountered
except KeyboardInterrupt:
	print('\nStoping...')
	sleep(1)