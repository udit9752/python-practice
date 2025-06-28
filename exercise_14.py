heights = input("Enter the heights of the students separated by spaces: ")
heights_list = heights.split()
# this will convert the list of strings to a string of integers
heights_list = [int(heights) for heights in heights_list]
# this will find the maximum heights
max_heights = max(heights_list)
# this wil find the maximum heights
min_heights = min(heights_list)
# this will find the average heights
avergae_heights = sum(heights_list)/len(heights_list)
print(f"the maximum heights is{max_heights}")
print(f"the maximum heights is{min_heights}")
print(f"the average heights is {avergae_heights}")
#this will find the number of students
num_students = len(heights_list)
