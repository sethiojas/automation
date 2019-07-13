import subprocess
import webbrowser


def set_alert_msg(status_code):
	''' determine which message to send as email alert based on the status code '''

	# Task status 		code (int)
	
	# Started 				0
	
	# Ended 				1
	
	# Authentication 		2
	# failure

	alert_msg = 'Subject: TASK STATUS\n'

	#task started email
	if status_code == 0:
		alert_msg += 'Started'
	
	#task ended email
	elif status_code == 1:
		alert_msg += 'Executed'
	
	#if email is not from allowed email address
	elif status_code == 2:
		alert_msg += 'COMMAND CAN NOT BE EXECUTED: AUTHENTICATION FAILURE'

	return alert_msg



def execute_task(command, soup):
	''' Execute the task received in email '''

	#if command is browser then fetch link and open it in default browser
	if command.lower() == 'browser':
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
	elif command.lower() == 'open':
		args = [member.get_text() for member in soup.findAll('div', dir='auto') if member.get_text() 
		not in ('\n','\r','\r\n') and not member.get_text().startswith('\n')]
		
		task = subprocess.Popen(args[0])
		task.wait()

	#if command matches exe then run executable with command line args
	elif command.lower() == 'exe':
		args = [member.get_text() for member in soup.findAll('div', dir='auto') if member.get_text() 
		not in ('\n','\r','\r\n') and not member.get_text().startswith('\n')]
		
		command_line_args = ' '.join(args[1:])
		task = subprocess.Popen([args[0], command_line_args])
		task.wait()

if __name__ == '__main__':
	main()