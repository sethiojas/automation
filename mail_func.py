import functions
import smtplib
import imapclient
import pyzmail
from time import sleep
from email.message import EmailMessage

class Mail():

	def __init__(self, bot_id, bot_passwd, receiver_id, allowed_email, sender_name):
		''' sets the parameters required to perform email related operation '''
		self.bot_id = bot_id
		self.bot_passwd = bot_passwd
		self.receiver_id = receiver_id
		self.allowed_email = allowed_email
		self.sender_name = sender_name
		self.command = None
		self.text_msg = None
		self.sent_mail = 0 #to track if any mail is sent by function other than the Task Started alert
		
		#set from, to and subject msgibutes of email
		self.email_msg = EmailMessage()
		self.email_msg['from'] = self.bot_id
		self.email_msg['to'] = self.receiver_id
		self.email_msg['subject'] = 'Task Status'


	def send_mail(self, status_code):
		''' Function to send send email alerts '''
		
		#Determine the appropriate message to send via email
		#depending upon task status
		email_alert = functions.set_alert_msg(status_code)

		#task deatils
		task_info = '\nTask Details\n' + self.command + '\n' +self.text_msg

		#message to be sent via email
		send_msg = email_alert + task_info

		#set body of email mssg
		self.email_msg.set_content(send_msg)
		
		#login into bot account
		mail = smtplib.SMTP('smtp.gmail.com', 587)
		mail.ehlo()
		mail.starttls()
		mail.login(self.bot_id, self.bot_passwd)

		#send mail
		mail.send_message(self.email_msg)

		#logout from bot id
		mail.quit()


	def read_mail(self):
		''' Function to read received email '''

		#login to bot email
		email_read = imapclient.IMAPClient('imap.gmail.com', ssl=True)
		email_read.login(self.bot_id, self.bot_passwd)
		
		#readonly is false because we want to be able
		#to delete emails which are read once
		email_read.select_folder('INBOX', readonly = False)
		
		#search email by allowed sender name
		uid = email_read.gmail_search(self.sender_name)

		command = None
		
		if uid: #if mail found
			print('Mail found')
			
			#get mail body
			#returns body in an encoded format
			raw = email_read.fetch(uid,'BODY[]')
			msg = pyzmail.PyzMessage.factory(raw[uid[0]][b'BODY[]'])

			#check if email address matches the allowed email
			#if not then set command equal to auth_fail and
			#text_msg = None
			if msg.get_addresses('from')[0][1] == self.allowed_email:
				
				command = msg.get_subject() #if true then command equals subject of email
			
				#get text form of mssg body
				text_msg = msg.text_part.get_payload().decode()
			else:
				command = 'auth_fail'
				text_msg = None
		 	
		 		
		 	#delete the read email
			email_read.delete_messages(uid[0])
			email_read.expunge()

		#If no mail is found by the name of sender (uid does not exists)
		else:
			print('No mail found')
			
		#logout from email
		email_read.logout()

		#If command is not None then save command and text_msg, 
		#also return both of them.
		#Otherwise return false to indicate that No email was found
		#as a result of search
		if command:
			self.command = command
			self.text_msg = text_msg
			return {'command': command,
					'text_msg': text_msg}
		return False

if __name__ == '__main__':
	main()