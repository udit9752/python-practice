import random
user_choice = int(input("Enter your choice 0 for rock, 1 for paper, 2 for scissors: "))
computer_choice = random.randint(0,2)
print("computer chois is:", computer_choice)
if user_choice == computer_choice:
    print("It's a tie!")
elif user_choice == 0 and computer_choice == 2:
    print("YOU WIN!")
elif user_choice == 1 and computer_choice == 0:
    print("You Win")
elif user_choice == 2 and computer_choice == 1:
    print("You Win")
else:
    print("You Lose")
if user_choice < 0 or user_choice > 2:  
    print("Invalid choice! Please enter 0, 1, or 2.")
elif computer_choice < 0 or computer_choice > 2:
    print("Invalid computer choice! Please check the random number generation.")
elif user_choice == 0:  
    print("You chose Rock.")
elif user_choice == 1:
    print("You chose Paper.")



