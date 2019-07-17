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
		self.mail_status = None
		
		#to track if any mail is sent by function other than the Task Started alert
		self.sent_mail = 0

		#set from, to and subject msgibutes of email
		self.email_msg = EmailMessage()
		self.email_msg['from'] = self.bot_id
		self.email_msg['to'] = self.receiver_id
		self.email_msg['subject'] = 'Task Status'


	def send_mail(self, status_code):
		''' Function to send send email alerts '''
		print('Sending mail ....')
		
		#Determine the appropriate message to send via email
		#depending upon status_code
		email_alert = functions.set_alert_msg(status_code)

		#task deatils
		task_info = '\n\nTask Details\n' + self.command + '\n' +self.text_msg

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
		print('Done')


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
		
		if uid: #if mail found
			print('Mail found')
			#raw form of mail
			raw = email_read.fetch(uid,'BODY[]')
			
			self.parse_mail(raw, uid)

			#delete the read email
			email_read.delete_messages(uid[0])
			email_read.expunge()
			
		#If no mail is found by the name of sender (uid does not exists)
		else:
			self.mail_status = 'not found'
			
		#logout from email
		email_read.logout()

		return self.status()

	def parse_mail(self, raw, uid):
		''' parse email and delete it afterwards '''
		msg = pyzmail.PyzMessage.factory(raw[uid[0]][b'BODY[]'])

		#check if email address matches the allowed email
		#and set the value of mail_status accordingly
		self.auth_mail(msg)
		
		#parse email
		self.command = msg.get_subject() 
		self.text_msg = msg.text_part.get_payload().decode()

	def auth_mail(self,msg):
		''' check if email is from allowed email address '''
		if msg.get_addresses('from')[0][1] == self.allowed_email:
			self.mail_status = 'found'
		else:
			self.mail_status = 'auth fail'

	def status(self):
		''' returns a string based on value of mail_status variable '''
		if self.mail_status == 'auth fail':
			return 'fail'

		elif self.mail_status == 'found':
			return {'command': self.command,
					'text_msg': self.text_msg}
		
		elif self.mail_status == 'not found':
			return False

if __name__ == '__main__':
	main()