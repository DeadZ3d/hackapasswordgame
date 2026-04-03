# 1. Input Validation of Password Input 

# INPUT VALIDATION
# ----------------

def inputValidation(password):
    # make sure there is no space at the front,
    # the back or in the middle of the string
    if " " in password:
        return True
    
    # make sure the string has at least 1 character 
    # and at most 16 characters
    elif len(password) < 1 or len(password) > 16:
        return True
    
    else:
        return False


# 2. Tokenize the string 
def tokenize_string(password): 
    tokens = list(password) 
    return tokens 


# 3. Get size of the string
def get_password_size(password):
    password_size = len(password)
    return password_size


# 4. Get digits and their locations
def get_digits_info(password):
    digits = []
    digit_positions = []

    for i, char in enumerate(password):
        if char.isdigit():
            digits.append(char)
            digit_positions.append(i)

    return digits, digit_positions


# 5. Get symbols and their locations
def get_symbols_info(password):
    symbols = []
    symbol_positions = []

    for i, char in enumerate(password):
        # Check if character is NOT alphanumeric (i.e., it's a symbol)
        if not char.isalnum():
            symbols.append(char)
            symbol_positions.append(i)

    return symbols, symbol_positions
