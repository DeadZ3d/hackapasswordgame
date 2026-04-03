import math

def estimate_poolsize(password):
    poolSize = 0

    has_lowercase = False
    has_uppercase = False
    has_digits = False
    has_symbols = False

    for character in password:
        if character.islower():
            has_lowercase = True
        elif character.isupper():
            has_uppercase = True
        elif character.isdigit():
            has_digits = True
        else:
            has_symbols = True

    if has_lowercase:
        poolSize += 26
    if has_uppercase:
        poolSize += 26
    if has_digits:
        poolSize += 10
    if has_symbols:
        poolSize += 32

    return poolSize

def entropy(password, leaked_list, english_dict):
    initial_entropy = 0
    length = len(password)
    pool = estimate_poolsize(password)

    WEIGHTL = 15 # Guess weight to the leaked list
    WEIGHTD = 5
    GPU_NUMS = 100
    GUESSES_PER_SECOND = 1000000000

    initial_entropy = length * math.log(pool, 2)
    print(f"Initial Entropy: {initial_entropy}")

    entropy_penalty = len(leaked_list) + WEIGHTL + len(english_dict) + WEIGHTD
    print(f"Entropy Penalty: {entropy_penalty}")

    adjusted_entropy = initial_entropy - entropy_penalty
    if adjusted_entropy < 0:
        adjusted_entropy = 0
    print(f"Adjusted Entropy: {adjusted_entropy}")

    # in seconds
    time = pow(2, (initial_entropy - entropy_penalty)) / (2 * GUESSES_PER_SECOND * GPU_NUMS)

    return time

