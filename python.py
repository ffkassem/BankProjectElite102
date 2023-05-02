# Imports
import mouse
import os
import random

# MySQL
import mysql.connector
connection = mysql.connector.connect(user = 'root', database = 'bankproject', password = 'password')
cursor = connection.cursor()

# User starts as not signed in
SignedIn = False
# Start user as not an admin
admin = False

account = 0


# Check if the input is a number
def numCheck(num):
    num_is_int = False
    # Try the input as a number
    try:
        int(num)
        # If the input is a number put num_is_int as True
        num_is_int = True
    except ValueError:
        print("\nTry again using a whole number")
        # If the input isn't a number put num_is_int as False
        num_is_int = False
    # Return num_is_int
    return num_is_int


# Check if the responce is yes
def yesNo(answer):
    yes = False
    if answer.lower() == "yes" or answer.lower() == "y":
        yes = True
    else:
        yes = False
    return yes


# Print out the choices a user has and let them choose one
def menu(userSignedIn, accountNum):
    print("\n\nSelect your choice:")
    if not userSignedIn:
        print("1. Login")
        print("2. Signup")
        print("3. Exit")
        upTo = 3
    else:
        print("1. Profile")
        print("2. Check Balance")
        print("3. Deposit Money")
        print("4. Withdraw Money")
        print("5. Logout")
        upTo = 5

    while True:
        choice = input(f"\nChoose an action from 1 - {upTo}: ")
        if choice.isdigit() and 0 < int(choice) <= upTo:
            if not userSignedIn:
                if int(choice) == 1:
                    signInNum = input("Account Number: ")
                    signInPin = input("Account PIN: ")
                    if login(signInNum, signInPin):
                        accountNum = signInNum
                        userSignedIn = True
                    else:
                        print("That is the wrong account or password")
                        print("Going back to the menu\n")
                        userSignedIn = False
                elif int(choice) == 2:
                    accountNum = createAccount()
                    userSignedIn = True
                    menu(userSignedIn, accountNum)
                elif int(choice) == 3:
                    print("...Exiting Program...")
                    break
            else:
                if int(choice) == 1:
                    print("...Loading profile...")
                    accountNum = checkProfile(accountNum)
                elif int(choice) == 2:
                    print("...Checking Balance...")
                    accountNum = checkBal(accountNum)
                elif int(choice) == 3:
                    userDeposit = input("\nHow much money do you want to deposit? ")
                    depositMon(userDeposit, accountNum)
                elif int(choice) == 4:
                    userWithdraw = input("\nHow much money do you want to withdraw? ")
                    withdrawMon(userWithdraw, accountNum)
                elif int(choice) == 5:
                    print("...Logging Out...")
                    userSignedIn = False
                    accountNum = 0
            menu(userSignedIn, accountNum)
        else:
            print("Invalid input, please enter a number from 1 to", upTo)



def createAccount():
    confirm = False
    while not confirm:
        print("Create a new account: ")
        # Start the account creation project
        userFirstName = input("\nFirst Name: ")
        # Ask user for last name
        userLastName = input("\nLast Name: ")
        # Ask user to confirm their choices if not clear screen and ask again
        responce = input("\nSay yes to confirm your choices? ")
        if not yesNo(responce):
            # If the user says no repeat the loop and clear the screen
            confirm = False

        else:
            # End the loop and continue
            confirm = True
    # Get the users pin using pin maker function
    currentpin = pinMaker()
    # Now get a pin
    newNum = False
    while not newNum:
        userNum = random.randint(3000, 9999999)
        print(userNum)
        newNum = True
        # add to the table if it is not the same number as another user
    # Tell the user their details
    print(f"Account Number: {userNum}")
    print(f"First Name: {userFirstName}")
    print(f"Last Name: {userLastName}")
    print(f"PIN: {currentpin}")
    responce = input("\nConfirm Account Details: ")
    if not yesNo(responce):
        # Make the user go back to the beginning of the function
        print("Ok then, put your information again.")
    else:
        print("...Loading...")
        # Add to table with balance at $0 by listing variables for function
        addAccount(userNum, userFirstName, userLastName, currentpin, 0)
        print("Account Created")


def pinMaker():
    passMatch = False
    # Print pins rules
    print("\nInsert a pin that is at least 4 digits long: \n")
    # while the pins don't match
    while not passMatch:
        # ask for a pin
        userInputPin = input("\nPin: ")
        # If pin is less than 4 don't accept pin
        if numCheck(userInputPin):
            if len(userInputPin) >= 4:
                # ask for pin confirmation
                userPinConf = input("\nConfirm pin: ")
                # check if the pin and confirmation match
                if userInputPin == userPinConf:
                    print("\nPin has been confirmed.")
                    return userInputPin
                else:
                    print("\nPins do not match. Please try again.")
            else:
                print("\nPin must be at least 4 digits long. Please try again.")
        else:
            print("\nInvalid input. Please try again.")

    passMatch = False

    # Print pins rules
    print("\nInsert a pin that is at least 4 digits long: \n")
    # while the pins don't match
    while not passMatch:
        # ask for a pin
        userInputPin = input("\nPin: ")
        # If pin is less than 4 don't accept pin
        if numCheck(userInputPin):
            if len(userInputPin) >= 4:
                # Ask user to confirm the pin
                userPinConfirm = input("Confirm pin: ")

                # Check if the pins are same
                if userInputPin == userPinConfirm:
                    print("Pins match.")
                    # Make passMatch into true to make the while statement end
                    passMatch = True
                else:
                    print("Pins do not match. \nTry Again")
                    passMatch = False
            else:
                print("Pin is too short try again")
                passMatch = False

            userPin = userInputPin
    # show the first and the last two characters of the pin
    # Remove two from the number so that you can show the pin with the right amount
    passNum = len(userPin) - 3
    passBlocked = userPin.split()[0][0] + "*" * passNum + userPin.split()[0][-1]
    yes_no = input(f"Confirm that you want to us this pin ('{passBlocked}')\n")
    if yesNo(yes_no):
        print("Ok, pin added to database")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        return userPin
    else:
        print("Ok, create a new pin!")
        # Run the pin maker again
        pinMaker()

def addAccount(AccNum, fName, lName, userPin, monAmount):
    addData = (f"INSERT INTO `bankproject`.`bank_project` (`Account_Num`, `first_name`, `last_name`, `PIN`, `balance`, `Admin`) VALUES ({AccNum}, '{fName}', '{lName}', '{userPin}', '{monAmount}', '0')")
    cursor.execute(addData)
    connection.commit()

def depositMon(amount, accountNum):
    addData = (f"UPDATE `bankproject`.`bank_project` SET `balance` = `balance` + '{amount}' WHERE (`Account_Num` = '{accountNum}');")
    cursor.execute(addData)
    connection.commit()

def withdrawMon(amount, accountNum):
    addData = (f"UPDATE `bankproject`.`bank_project` SET `balance` = `balance` - '{amount}' WHERE (`Account_Num` = '{accountNum}');")
    cursor.execute(addData)
    connection.commit()

def checkBal(account_Num):
    accountNum = account_Num
    query = ("SELECT balance FROM bank_project WHERE Account_Num = %s")
    cursor.execute(query, (accountNum,))

    # Fetch the balance from the result set
    result = cursor.fetchone()
    print(f"Current balance for account number, {accountNum} is:", result[0])

    return accountNum

# Show the row for that profile
def checkProfile(account_Num):
    accountNum = account_Num
    query = (f"SELECT * FROM bank_project WHERE {accountNum} = %s")
    cursor.execute(query, (accountNum,))

    # Fetch the balance from the result set
    result = cursor.fetchone()
    print("Account Number: ", result[0])
    print("First name: ", result[1])
    print("Last name: ", result[2])
    print("Pin: ", result[3])
    print("Balance: ", result[4])

    return account_Num
    


def login(account_num, pin):

    # Execute a SELECT statement to retrieve the user with the given account number and pin
    query = "SELECT * FROM bank_project WHERE account_num = %s AND pin = %s"
    cursor.execute(query, (account_num, pin))
    user = cursor.fetchone()

    # If a user with the given credentials exists, return True. Otherwise, return False.
    if user:
        return True
    else:
        return False


# """ This is used to test code (delete when finished)"""
# checkBal(3350910)


userSignedIn = False

# Welcome the user to the app
print("Hello, welcome to the Blank Bank Place App!")

menu(SignedIn, account)

cursor.close()

connection.close()
