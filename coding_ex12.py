import random
name = input("Entr the name of the all the participants (separated by commas): ")
participents = name.split(",")
print(participents)
name_len = len(participents)
name_choice = random.randint(0, name_len -1)
print(f"the {participents[name_choice]} pay the bill")
