# GMail API to get mails and move to folders

Assignment for HappyFox

# Introduction:

This project is developed to get a list of mails for the user and process them for rules defined already and move them to appropriate folders using GMail API. 

This project is developed in Python 3.7. OAuth is used to authorize GMail API, Google's official python client for GMail API.
MySQL is used for storing mails in the database. Rules are stored in a JSON file and it is used for processing the mails in the Database. 

# Installation:

Tested working with Linux system - Ubuntu 16.04 LTS

1. Install MySQL server and set user name and password by following the steps below,
  
  sudo apt-get install mysql-server
  mysql_secure_installation

2. Install python-pip3 by the steps below,

  sudo apt-get install python3-pip

3. Install virtualenv by,

  sudo pip3 install virtualenv 

4. Create a virtualenv in the path you wish using,

  virtualenv -p python3 <your environment name> 

5. Activate the virtualenv

  source <your environment name>/bin/activate


# Usage:

1. Enable the GMail API and allow access to your project to use GMail API for getting mails and updating them.
2. Use the rules.json to create the rules that should be followed for the mails that are fetched from the API.
3. Run the file read_mail.py to get the mails, store them and then apply the rules on the mails and update the mails.

