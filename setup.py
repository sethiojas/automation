import shelve
from simplecrypt import encrypt
from os import system
import getpass

#get the required credentials and data
bot_id = input('Bot Email ID> ')
bot_passwd = getpass.getpass(f'Password for {bot_id}> ')

system('clear')
receiver_id = input('Receive email alerts on this ID> ')
allowed_email = input('Only follow instructions given via this email ID> ')
sender_name = input(f'First Name account owner of {allowed_email}> ')
download_path = input('Download email attachments(if present) to this directory'
					'\neg: /path/to/directory  (correct)'
					'\n    /path/to/directory/ (wrong)'
					'\n> ')
master = getpass.getpass('Enter master password> ')

system('clear')

#saves them in dictionary
data = {
	'bot_id':bot_id,
	'bot_passwd':bot_passwd,
	'receiver_id':receiver_id,
	'allowed_email':allowed_email,
	'sender_name':sender_name,
	'download_path':download_path
}

#encrypt the values of corresponding keys
print('Encrypting data....')
for key, value in data.items():
	print(f'Encrypting {key}....')
	data[key] = encrypt(master, value)
	print('Done')
print('Encryption Done')

#save the dictionary in shelve file
print('Saving data')
sv = shelve.open('data')
sv['data'] = data
sv.close()