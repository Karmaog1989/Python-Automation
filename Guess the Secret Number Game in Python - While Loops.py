#Using While Loop for Guess the Secret Number Game in Python
#Added random number generator

import random 
secret_number = random.randint(1, 10)
max_attempts = 3
attempts = 0


while attempts < max_attempts:
    try:
        guess = int(input("Guess the secret number between 1 and 10: "))
        attempts += 1
        if guess > 10 or guess < 1:
            print("Please input a number between 1 and 10")
            continue

        if guess == secret_number:
            print(f"Success! The secret number is {secret_number}")
            break

        else:
            if guess > secret_number:
                print("Too high!")
            elif guess < secret_number:
                print("Too low!")

    except:
        print("Please enter a valid number between 1 and 10")
# If the loop ends without guessing correctly
else:
    print(f"Out of attempts! The secret number was {secret_number}.")
