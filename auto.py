#!/usr/bin/python3

from time import sleep
import imapclient
import pyzmail
import smtplib
from bs4 import BeautifulSoup
import subprocess
import threading
import webbrowser
from os import system


def send_mail(status, msg):
	
	mail = smtplib.SMTP('smtp.gmail.com', 587)
	mail.ehlo()
	mail.starttls()
	mail.login('@gmail.com', '')     # <-------------------ADD
	if status == 0:
		mail.sendmail('@gmail.com', '@outlook.com', # <-----ADD
			'Subject: TASK STATUS\nStarted')
	elif status == 1:
		mail.sendmail('@gmail.com', '@outlook.com',# <------ADD
			'Subject: TASK STATUS\nExecuted')
	mail.quit()

	print(msg)


try:
	while True:
		active_threads = []
		
		system('clear')
		print('Logging In....')
		
		email_read = imapclient.IMAPClient('imap.gmail.com', ssl=True)
		email_read.login('@gmail.com', '') # <------------ADD
		email_read.select_folder('INBOX', readonly = False)
		uid = email_read.gmail_search('')# <--------------ADD
		if uid:
			print('Mail found')
			
			raw = email_read.fetch(uid,'BODY[]')
			msg = pyzmail.PyzMessage.factory(raw[uid[0]][b'BODY[]'])
			
			if msg.get_addresses('from')[0][1] == '@outlook.com': # <-------ADD
				command = msg.get_subject()
			else:
				command = None
			
			text = msg.html_part.get_payload().decode()
		 	
			email_read.delete_messages(uid[0])
			email_read.expunge()
			
			email_read.logout()

			if command:
				print("Task Status : START")
				thread_mail = threading.Thread(target = send_mail, args = [0, 'Mail Sent : START status'])
				active_threads.append(thread_mail)
				thread_mail.start()
			

			soup = BeautifulSoup(text, 'html.parser')
			
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

			elif command in ('open', 'Open', 'OPEN'):
				args = [member.get_text() for member in soup.findAll('div', dir='auto') if member.get_text() 
				not in ('\n','\r','\r\n') and not member.get_text().startswith('\n')]
				
				task = subprocess.Popen(args[0])
				task.wait()

			elif command in ('exe', 'Exe', 'EXE'):
				args = [member.get_text() for member in soup.findAll('div', dir='auto') if member.get_text() 
				not in ('\n','\r','\r\n') and not member.get_text().startswith('\n')]
				 
				task = subprocess.Popen([args[0], args[1]])
				task.wait()

			if command:
				print("Task Status : ENDED")
				thread_mail = threading.Thread(target = send_mail, args = [1, 'Mail sent : ENDED status'])
				active_threads.append(thread_mail)
				thread_mail.start()
		
		else:
			print('No mail found')
		
		for threads in active_threads:
			threads.join()
		
		sleep(5)
		system('clear')
		print('Sleeping....')
		
		sleep(300)

except KeyboardInterrupt:
	print('\nStoping...')
	sleep(1)