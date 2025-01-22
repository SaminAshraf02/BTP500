import time
import random

print("\nCourse code: BTP500 Data Structures and Algorithms")
print("Student name: Samin Ashraf")
print("Student ID: 140362229\n")

# Function to create a list of random integers of size n
def sorted_list_creator(n):

    i = 0
    int_array = []

    while n > 0 and i < n:

        i += 1
        generated_random_integer = random.randint(1, 100)
        int_array.append(generated_random_integer)

    n = len(int_array)

    for i in range(n - 1):

        min_index = i

        for j in range(i + 1, n):

            if int_array[j] < int_array[min_index]:

                min_index = j


        if min_index != i:

            int_array[min_index], int_array[i] = int_array[i], int_array[min_index]

    return int_array

def linear_search(my_list, key):

    for i in range(0, len(my_list)):

        if my_list[i] == key:

            return i

    return -1

def binary_search(my_list, key):
    low_index = 0
    high_index = len(my_list) - 1

    while low_index <= high_index:

        mid_index = (low_index + high_index) // 2

        if key == my_list[mid_index]:
            return mid_index
        elif key < my_list[mid_index]:
            high_index = mid_index - 1
        else:
            low_index = mid_index + 1

    return -1

