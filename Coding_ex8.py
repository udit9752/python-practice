age = int(input("Enter your age: "))

if age < 10:
    print("Sorry, you are too young to ride.")
elif age < 18:
    print("You can ride.")
    bill = 250
    print("Pay 250 rupees.")
    selfies = input("Do you want to take selfies? (Y/N): ")
    if selfies.lower() == "y":
        print("Pay 100 rupees for selfies.")
        bill += 100
    print("Total bill is", bill)
else:
    print("You can ride.")
    bill = 500
    print("Pay 500 rupees.")
    selfies = input("Do you want to take selfies? (Y/N): ")
    if selfies.lower() == "y":
        print("Pay 100 rupees for selfies.")
        bill += 100
    print("Total bill is", bill)
