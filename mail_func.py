import functions
import smtplib
import imapclient
import email
from time import sleep
from email.message import EmailMessage
import re

class Mail():

	def __init__(self, bot_id, bot_passwd, receiver_id, allowed_email, sender_name):
		''' sets the parameters required to perform email related operation '''
		self.bot_id = bot_id
		self.bot_passwd = bot_passwd
		self.receiver_id = receiver_id
		self.allowed_email = allowed_email
		self.sender_name = sender_name
		
		#to track if any mail is sent by program in between the Task Started alert
		#and Task Executed alert emails
		self.sent_mail = 0

		self.command = None
		self.text_msg = None

		self.create_message_obj()

	def create_message_obj(self):
		'''set from, to and subject message atributes of email'''
		self.email_msg = EmailMessage()
		self.email_msg['from'] = self.bot_id
		self.email_msg['to'] = self.receiver_id
		self.email_msg['subject'] = 'Email Notification'

	def send_mail(self, status_code):
		''' Function to send send email alerts '''
		print('Sending mail ....')
		
		#appropriate message to send via email is determined via value of
		#status code which is  passed as an argument to set_alert_msg function.
		#set_alert_msg function returns a string which is concatinated with
		#the contents of email which was received (stored in variable task_info).
		#This new string is stored in send_msg variable and forms the body of
		#the email which the program sends.
		
		email_alert = functions.set_alert_msg(status_code)
		task_info = '\n\nTask Details\n' + self.command + '\n' +self.text_msg

		send_msg = email_alert + task_info
		self.email_msg.set_content(send_msg)
	
		mail = smtplib.SMTP('smtp.gmail.com', 587)
		mail.ehlo()
		mail.starttls()
		mail.login(self.bot_id, self.bot_passwd)

		mail.send_message(self.email_msg)

		mail.quit()
		print('Done')


	def read_mail(self):
		''' Function to read received email '''

		#log int the email account of bot and search for emails with sender_name as parameter
		#list of IDs found as a result of gmail_search() are passed as an argument
		#to parse_mail function. The value returned by parse_mail function is stored
		#in response variable which is then returned to the calling function

		email_read = imapclient.IMAPClient('imap.gmail.com', ssl=True)
		email_read.login(self.bot_id, self.bot_passwd)
		email_read.select_folder('INBOX', readonly = False)
		uid = email_read.gmail_search(self.sender_name)

		response = self.parse_mail(email_read, uid)

		email_read.logout()
		return response


	def parse_mail(self, email_read, uid):

		#if uid is an empty list that means no email was found as a result of search
		#hence false is returned to indicate the same. If uid is not empty then
		#authentication of mail is carried out. If auth. succeedes mail is parsed
		#if it fails then 'fail' is returned
		
		if uid:
			print('Mail found')
			
			raw = email_read.fetch(uid, b'RFC822')
			msg = email.message_from_bytes(raw[uid[0]][b'RFC822'])
			if self.auth_mail(msg):
				self.command = msg.get('Subject')
				for item in msg.walk():
					if item.get_content_type() == 'text/plain':
						self.text_msg = item.get_payload(decode = True)
						self.text_msg = self.text_msg.decode()#needed as otherwise results into TypeError in send_mail function
				
				#delete the read email
				email_read.delete_messages(uid[0])
				email_read.expunge()

				return {'command':self.command, 'text_msg':self.text_msg}
			return 'fail'
		return False
		

	def auth_mail(self,msg):
		''' check if email is from allowed email address '''

		#mail_from is string of type ``` FirstName LastName <email@domain.com> ```
		#to extract characters between < and > , we use regular expression
		 
		find_mail = re.compile(r'<(.*)>')
		mail_from = msg.get('From')
		if find_mail.search(mail_from).group(1) == self.allowed_email:
			return True
		return False

if __name__ == '__main__':
	main()