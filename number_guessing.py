from bdb import Breakpoint
import random


name = input("Hey there! What is your name?")
def game():
    tries = int(input(f"Hello {name}! How many attempts do you want?"))
    number = random.randint(0,20)
    attempt = 0
    success = 0
    while attempt < tries:
        guess = int(input(f"Take a Guess {name}!"))
        attempt +=1
        if guess < number:
            print(f"Number is too Low.")
        elif guess > number:
            print(f"Number is too High.")
        else:
            print(f"{name} you guessed right! Hurray!!!")
            print(f"{name} you took {attempt} attempts.")
            success = 1
            break
    if success ==0:
        print(f"Sorry {name}, you lost this game. Better luck next time.")
        print(f"My number was {number}.")

def main():
    game()
    while True:
        another = input("Do you wish to play again?(Y/N)")
        if another.lower() == "y":
            game()
        else:
            break

main()