# Automation
## Table of Contents
* [About](#about)
* [Installation](#installation)
* [Modules Used](#modules-used)
* [Examples](#examples)

## About
This a program aimed at remotely controlling your computer via email instructions.
This program needs a spare GMAIL id to work.
***IMPORTATNT : ENABLE 'ALLOW LESS SECURE APPS TO ACCESS YOUR ACCOUNT' IN THE GMAIL ACCOUNT***
Instructions can be sent to this spare GMAIL id via only a pre-specified email address.
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