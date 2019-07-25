import functions
import smtplib
import imapclient
import email
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
		
		#to track if any mail is sent by function other than the Task Started alert
		self.sent_mail = 0

		self.command = None
		self.text_msg = None

		self.create_message_obj()

	def create_message_obj(self):
		'''#set from, to and subject message atributes of email'''
		self.email_msg = EmailMessage()
		self.email_msg['from'] = self.bot_id
		self.email_msg['to'] = self.receiver_id
		self.email_msg['subject'] = 'Email Notification'

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

		response = self.parse_mail(uid)

		#logout from email
		email_read.logout()

		return response


	def parse_mail(self, uid):
		
		if uid: #if mail found
			print('Mail found')
			
			#check if email address matches the allowed email
			#if it is not, Then return 'fail'
			if self.auth_mail(msg):
			
				#raw form of mail
				raw = email_read.fetch(uid, b'RFC822')
				
				''' parse email and delete it afterwards '''
				msg = email.message_from_bytes(raw[uid[0]][b'RFC822'])

				self.command = msg.get('Subject')
				for item in msg.walk():
					if item.content_type() == 'text/plain':
						self.text_msg = item.get_payload(decode = True)

				#delete the read email
				email_read.delete_messages(uid[0])
				email_read.expunge()

				return {'command':self.command, 'text_msg':self.text_msg}

			else:
				return 'fail'
			
		#If no mail is found by the name of sender (uid does not exists)
		#then return False
		else:
			return False
		

	def auth_mail(self,msg):
		''' check if email is from allowed email address '''
		if msg.get_addresses('from')[0][1] == self.allowed_email:
			return True
		else:
			return False

if __name__ == '__main__':
	main()