#NUMBER GUESSING GAME
import random
tot_attempts=7
def guess_number(num):
    for attempt in range(1, tot_attempts + 1):
        guess = int(input("Guess a number: "))
        if guess==num:
            print("correct Guess!!")
            print("Total attempts =", attempt)
            return
        elif guess>num:
            print("too high")
        elif num>guess:
            print("too low")
        if abs(guess-num)<=5:
            print("But you're very close!")
        print("Attempts left:", tot_attempts - attempt)
    print("Out of attempts! The number was", num)

while True:
    print("NUMBER GUESSING GAME\n select level:\n 1.Easy(between 1-50)\t 2.Medium(between 1-100)\t 3.Difficult (between 1-150)")
    print("You have", tot_attempts, "attempts to win")
    ch=int(input("Enter level for game(1-3):"))
    if ch==1:
        num=random.randint(1,50)
    elif ch==2:
        num=random.randint(1,100)
    elif ch==3:
        num=random.randint(1,150)
    else:
        print("Invalid level, try again.")
        continue
    guess_number(num)
    again = input("Play again? (y/n): ")
    if again.lower() != "y":
        print("Thanks for playing!")
        break
