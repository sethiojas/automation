import functions
import smtplib
import imapclient
import email
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage
import re
import os
import datetime

class Mail():

	def __init__(self, bot_id, bot_passwd, receiver_id, allowed_email, sender_name, download_path):
		''' sets the parameters required to perform email related operation '''
		self.bot_id = bot_id
		self.bot_passwd = bot_passwd
		self.receiver_id = receiver_id
		self.allowed_email = allowed_email
		self.sender_name = sender_name
		self.download_path = download_path
		
		#to track if any mail is sent by program in between the Task Started alert
		#and Task Executed alert emails
		self.sent_mail = 0

		self.command = None
		self.text_msg = None

	def create_message_obj(self):
		'''set from, to and subject message atributes of email'''
		
		self.email_msg['from'] = self.bot_id
		self.email_msg['to'] = self.receiver_id
		self.email_msg['subject'] = 'Email Notification'

	def send_mail(self, status_code):
		''' Function to send send email alerts '''
		
		#create_message_body create the body of the email
		#which is sent to the receiver_id by this function
		
		print('Sending mail ....')
		body = self.create_email_body(status_code)
		if status_code == 5:
			self.email_msg.attach(MIMEText(body))
		else:
			self.email_msg.set_content(body)
		mail = smtplib.SMTP('smtp.gmail.com', 587)
		mail.ehlo()
		mail.starttls()
		mail.login(self.bot_id, self.bot_passwd)

		mail.send_message(self.email_msg)

		mail.quit()
		print('Done')

	def create_email_body(self, status_code):
		''' Function to create body of email '''

		#appropriate message to send via email is determined via value of
		#status code which is  passed as an argument to set_alert_msg function.
		#set_alert_msg function returns a string which is concatinated with
		#the contents of email which was received (stored in variable task_info).
		#This new string is stored in send_msg variable and forms the body of
		#the email which the program sends.

		if status_code != 5:
			self.email_msg = EmailMessage()	
		
		self.create_message_obj()
		email_alert = functions.set_alert_msg(status_code)
		#convert command and text_msg to str so that concatination can take place even if they have None value
		task_info = '\n\nTask Details\nCommand :\t'+str(self.command) + '\nBody :\t' +str(self.text_msg)

		send_msg = email_alert + task_info
		return send_msg



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

					self.download_attachments(item)
				
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
		if find_mail.search(mail_from).group(1) in self.allowed_email:
			return True
		return False

	def download_attachments(self, item):
		''' download attachments from email (if present) '''
		
		#functions checks is attachment(s) is present, if it is present then
		#it downloads attachment(s) to specified directory.
		#Directory is created if it does not already exists
		#if a file with same name is present in the given directory
		#then date and time is append at the at the end of the name of
		#newly downloaded file
		
		if item.get('Content-Disposition') == None:
			return None
		filename = item.get_filename()
		path = os.path.join(self.download_path, filename)
		if not os.path.exists(self.download_path):
			os.mkdir(self.download_path)
		if os.path.exists(path):
			path = path + str(datetime.datetime.now())
		with open(path, 'wb') as file:
			file.write(item.get_payload(decode = True))

	def send_attachment(self, args):
		''' Send files via email '''

		#function goes through the list of path provided in the mail body
		#and checks if the path exists. If the path is valid then the file
		#whose path is provided is added as an attachment to the email notification
		#with the same name by which it is stored on the user's computer

		self.email_msg = MIMEMultipart()
		for path in args:
			if os.path.exists(path):
				with open(path, 'rb') as file:
					part = MIMEApplication(
						file.read(),
						Name = os.path.basename(path))
				# part['Content-Disposition'] = f'attachment; filename="{os.path.basename(path)}" '
				part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(path))
				self.email_msg.attach(part)
		self.sent_mail = 1	
		status_code = 5
		self.send_mail(status_code)


if __name__ == '__main__':
	main()