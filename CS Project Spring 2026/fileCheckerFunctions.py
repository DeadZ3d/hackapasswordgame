# Nwabueze-Umeh Izuchukwu's functions that checks files
#|
#|
#|
# where 'password' is the user_input

import re


# check if a leaked password from the leaked passwor file is in the password
def existingPasswordChecker(password, matchedList):
     # regex that matches only if the entire line is alphanumeric
    pattern = re.compile(r'^[a-zA-Z0-9]+$')
    
    with open('rockyou.txt', 'r', encoding = "latin-1", errors = "ignore") as f:
        for line in f:
            cleanLine = line.strip()
            if not cleanLine:  # skip empty lines
                continue
                
            # check if line is purely alphanumeric
            if pattern.match(cleanLine):

                # check if the line is in the password
                if cleanLine in password:
                    matchedList.append(cleanLine)
                    
    return matchedList



# check if an english word is in the password from the english words file 
def englishWordsChecker(password, matchedList):
    # regex that matches if the entire line is alphanumeric
    pattern = re.compile(r"^[a-zA-Z0-9]+$")
    
    with open('english_words.txt', 'r', encoding = "latin-1", errors = "ignore") as f:
        for line in f:
            cleanLine = line.strip()
            if not cleanLine:  # skip empty lines
                continue
                
            # check if line is purely alphanumeric
            if pattern.match(cleanLine):
                # check if the line is in the password
                if cleanLine.lower() in password.lower(): # ignore case because of the english words
                    matchedList.append(cleanLine)
    
    return matchedList



# get a list of passwords in the leaked password files that are in the password from the user
leakedPasswordList = []
commonPasswords = existingPasswordChecker(password, leakedPasswordList)

# get a list of the english words in the password
englishWordsList = []
englishWords = englishWordsChecker(password, englishWordsList)
