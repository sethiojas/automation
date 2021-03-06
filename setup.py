import shelve
from simplecrypt import encrypt
from os import system
import getpass
import sys
from tqdm import tqdm

#User is prompted for required credentials for the functioning of automate.py
#A master password is set to lock the data. User has to Re-enter the master password
#for program to save data. 3 attempts are given to user to make the master2 match the
#master password. 3 failed attempts stop the program and data is discarded.
#Upon successful setting-up of master password the credentials are encrypted and saved
#in a pickle file named `data`.


#Get required data
system('clear')
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

master = getpass.getpass('Enter master password (You will be asked to enter this at every program run)\n> ')

master2 = getpass.getpass('Re-Enter master password> ')

attempts = 3
while master != master2 and attempts > 0:
	print(f"Passwords do not match. Attempts left {attempts}")
	master2 = getpass.getpass('Re-Enter master password> ')
	attempts -=1

if attempts == 0:
	sys.exit("PASSWORD FAILURE : EXITING")
system('clear')

#save data in a dictionary
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

for key, value in tqdm(data.items()):
	data[key] = encrypt(master, value)
print('Encryption Done')

#save the dictionary in shelve file
sv = shelve.open('data')
sv['data'] = data
sv.close()