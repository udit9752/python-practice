size = input("What is the size of the pizza you want to order? (S,M,L): ")
bill = 0
if size == "S" or size == "s":
   bill  = 100
elif size == "M" or size == "m":
    bill = 200
elif size == "L" or size == "l":
    bill = 300
else:
    print("Invalid size entered.")
add_pepperoni = input("Do you want t add pepperoni? (Y/N):")
if add_pepperoni == "Y" or add_pepperoni == "y":
    if size == "S" or size == "s":
        bill +=50
    elif size == "M" or size == "m":
        bill += 100
    elif size == "L" or size == "l":
        bill += 150
add_cheese = input("Do you want t add extra cheese? (Y/N):")
if add_cheese == "Y" or add_cheese == "y":
    bill += 50
    print(f"Your total bill is {bill} rupees.")
    print("success fully ")
