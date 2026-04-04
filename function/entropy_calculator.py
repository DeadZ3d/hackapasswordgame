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
    length = len(password)
    pool = estimate_poolsize(password)

    WEIGHTL = 15
    WEIGHTD = 5
    GPU_NUMS = [10, 100, 1000, 1000000]
    GUESSES_PER_SECOND = 1000000000

    if pool == 0:
        return {}

    initial_entropy = length * math.log(pool, 2)
    print(f"Initial Entropy: {initial_entropy}")

    unique_leaked_matches = list(set(leaked_list))
    unique_english_matches = list(set(english_dict))

    leaked_penalty = 0
    english_penalty = 0

    # Apply one penalty for each type of weakness instead of one penalty
    # for every overlapping substring that was found.
    if len(unique_leaked_matches) > 0:
        leaked_penalty = WEIGHTL

    if len(unique_english_matches) > 0:
        english_penalty = WEIGHTD

    entropy_penalty = leaked_penalty + english_penalty
    print(f"Entropy Penalty: {entropy_penalty}")

    adjusted_entropy = initial_entropy - entropy_penalty
    if adjusted_entropy < 0:
        adjusted_entropy = 0
    print(f"Adjusted Entropy: {adjusted_entropy}")

    crack_times = {}

    for gpu_count in GPU_NUMS:
        time = pow(2, adjusted_entropy) / (2 * GUESSES_PER_SECOND * gpu_count)
        crack_times[gpu_count] = time

    return crack_times
