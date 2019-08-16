# Automation
## Table of Contents
* [About](#about)
* [Installation](#installation)
* [Modules Used](#modules-used)
* [Valid Email Subjects](#valid-email-subjects)
* [Examples](#examples)
* [Easter-Egg](#easter-egg)
* [To-Do's](#to-do's)

## About
This a program aimed at remotely controlling your computer via email instructions.
This program needs a spare GMAIL id which works as a bot id for this program.

***IMPORTATNT : ENABLE 'ALLOW LESS SECURE APPS TO ACCESS YOUR ACCOUNT' IN THE GMAIL ACCOUNT***

Instructions can be sent to this spare GMAIL id (bot id) via only a pre-specified email address.
Instructions from emails other than the pre-specified email are marked as unauthorized.

## Installation
***Note : This program was build on Python 3.7.3***
1. Open the terminal

2. Move into the directory where the files are stored.
`cd path/to/automation/directory/`

3. Run `setup.py` file.
` python setup.py`

4. Fill the information/credentials as asked by the program.

5. Program is ready to run. To run the program, go to the directory where the project is stored
and run automate.py.
```
cd path/to/automation/directory/
python automate.py
```
## Modules Used
* subprocess
* time
* webbrowser
* functools
* os
* shelve
* simplecrypt
* getpass
* smtplib
* imapclient
* email
* re
* datetime

## Valid Email Subjects
* [browser](#browser)
* [exe](#exe)
* [send](#send)
* [stop](#stop)
* [sleep](#sleep)
* [list](#list)

* ### Browser
Used to open links in the default browser of your system.
Links should be seperated by newlines in the email body

* ### Exe
Opens the executable file at the given path.
Command line arguments can be provided for python scripts that utilize **sys.argv** method of argument parsing.
Email body should contain Data in this order :
1. path/to/executable/
2. command line arguments for python script

***Note: everything should be seperated by newlines***

* ### Send
Get file via email from your system.
The body should contain the path to file.
***The path given must not be of a directory***

* ### Sleep
Change the amount of delay time after parsing one email.
The default is 120 seconds.
i.e. the program sleeps for 120 seconds after reading/executing one email/task respectively

* ### Stop
Remotely stop the execution of automate.py.
Email body could be left empty.

***Time should be specified in seconds in the email body***

A command such as
``` 
subject : sleep
body : 2
```
will set the delay time of 2 seconds, not 2 minutes.

* ### List
Sends the list of all the files/directories stored at a given path.
```
home
  |this
    |1.jpg
	|hello
	  |eg.txt
	|yes.mp4
```
An email such as
```
subject : list
body : home/this
```
will result in an email that will look like this

```
f--1.jpg
d--hello
f--yes.mp
```
where 'f' denotes file and 'd' denotes directory.

## Easter Egg
**Find out what happens if the email subject is not one of the Valid email Subjects. The result may be different everytime
(just saying)**

## To-Do's
* [ ] Check if Path given is directory \(send command\).
* [ ] Send Contents of whole directory via email.
* [x] Add option to remotely stop Program.
