check = inputValidation(password)

    # if invalid, ask the user for valid password
    while check:
        password = input("Invalid Password. Try another one: ")
        check = inputValidation(password)
