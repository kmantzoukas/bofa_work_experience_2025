
import sys
import random
import os
from random import randrange
import bofa

# The user initally is logged out
_loggedIn = False
# A random balance is being set when the program starts
_balance = round(random.uniform(1,100), 2)
# The accound id is a unique identifier for each account that will be used when sending funds from one account to another
_accountId = bofa.generateId()
# Teh username of the user is the same as the account id
_username = _accountId
_password = "s3cret"
# A random currency is picked for each 
_currency = ["USD","GBP","EUR"][random.randint(0,2)]

# User commands to be implemented
def login(usr, pwd) -> bool:
    global _loggedIn
    global _username
    global _password
    if _loggedIn:
        return True
    else:
        if usr == _username and pwd == _password:
            _loggedIn = True
            return _loggedIn
        else:
           return False
def exit() -> None:
    global _accountId
    if os.path.exists('accounts_file_db/' + _accountId):
        os.remove(_accountId)
    print('Thanks for using the Fund Transfer Application. See ya later!')   
    sys.exit(0)
def deposit(amnt: float) -> None:
    global _balance
    _balance = _balance + amnt
    print('The funds have been deposited successfully.')
def send(accountId: str,amount: float) -> None:
    global _balance
    global _accountId
    global _currency
    _balance = bofa.updateBalance(_balance, _accountId, _currency)
    if amount > _balance:
        print('You do not have sufficient funds in your account.')
    else:
        _balance = _balance - amount
        with open('accounts_file_db/' + accountId, "a+") as f:
            f.write(str(amount) + " " + _currency + "\n")
        print('The funds have been sent successfully.')
def balance() -> None:
    global _balance
    global _accountId
    global _currency
    _balance = bofa.updateBalance(_balance, _accountId, _currency)
    print('You account balance is %s %s' % (_balance, _currency))

bofa.printWelcomeMessage(_accountId,_balance,_currency)

while True:
    user_input = input('\nWhat do you want to do next? Type help to see all the available options\n > ')
    command = user_input.split(" ")[0].lower()
    if command == 'exit':
        exit()
        
    elif command == 'login':
        try:
            usr: str = user_input.split(" ")[1]
            pwd: str = user_input.split(" ")[2]
            if login(usr, pwd):
                print('Congratulations, You have logged in successfully.')
            else:
                print('The credentials you have provided are not correct. Please try again!')
        except Exception as e:
            print('Oops! There has been an unexpected error with your command. Please try again!')
        

    elif command == 'send':
        try:
            if _loggedIn:
                accountId = user_input.split(" ")[1]
                amount = user_input.split(" ")[2]
                send(str(accountId),float(amount))
            else:
                print('You have to login first before you can run this command')
        except Exception as e:
            print('Oops! There has been an unexpected error with your command. Please try again!')         
        
    elif command == 'help':
        bofa.help()
        
    elif command == 'balance':
        balance()
        
    elif command == 'deposit':
        try:
            if _loggedIn:
                amount = float(user_input.split(" ")[1])
                deposit(amount)
            else:
                print('You have to login first before you can run this command')
        except Exception as e:
            print('Oops! There has been an unexpected error with your command. Please try again!')        
    
    else:
        print('The command you typed in is not valid. Please try again!')
