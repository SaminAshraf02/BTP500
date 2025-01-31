import time
import random

print("\nCourse code: BTP500 Data Structures and Algorithms")
print("Student name: Samin Ashraf")
print("Student ID: 140362229\n")

# Function to create a list of random integers of size n
def array_creator(n):

    i = 0
    int_array = []

    while n > 0 and i < n:

        i += 1
        generated_random_integer = random.randint(1, 100)
        int_array.append(generated_random_integer)

    return int_array

# Insertion sort function
def insertion_sort(my_list):

    for i in range(0, len(my_list)):

        current = my_list[i]
        j = i

        while j > 0 and my_list[j - 1] > current:

            my_list[j] = my_list[j - 1]
            j -= 1

        my_list[j] = current

# Bubble sort function
def bubble_sort(my_list):

    n = len(my_list)

    for i in range(n - 1):

        for j in range(n - 1 - i):

            if my_list[j] > my_list[j + 1]:

                my_list[j], my_list[j + 1] = my_list[j + 1], my_list[j]

# Selection sort function
def selection_sort(my_list):

    n = len(my_list)

    for i in range(n - 1):

        min_index = i

        for j in range(i + 1, n):

            if my_list[j] < my_list[min_index]:

                min_index = j


        if min_index != i:

            my_list[min_index], my_list[i] = my_list[i], my_list[min_index]

# Test cases
j = 0

while j <= 2:
    
    sample_size = [100, 200, 300]
    times = []
    n = sample_size[j]
    j += 1

    generated_integer_array = array_creator(n)
    insertion_sort_array = list(generated_integer_array)
    bubble_sort_array = list(generated_integer_array)
    selection_sort_array = list(generated_integer_array)

    start_time = time.perf_counter()
    insertion_sort(insertion_sort_array)
    end_time = time.perf_counter()
    time_taken = end_time - start_time
    times.append(time_taken)
    print(f"Sample size = {n}, Algorithm = Insertion Sort, Time taken = {time_taken} second(s)")

    start_time = time.perf_counter()
    bubble_sort(bubble_sort_array)
    end_time = time.perf_counter()
    time_taken = end_time - start_time
    times.append(time_taken)
    print(f"Sample size = {n}, Algorithm = Bubble Sort,    Time taken = {time_taken} second(s)")

    start_time = time.perf_counter()
    selection_sort(selection_sort_array)
    end_time = time.perf_counter()
    time_taken = end_time - start_time
    times.append(time_taken)
    print(f"Sample size = {n}, Algorithm = Selection Sort, Time taken = {time_taken} second(s)")

    if (times[0] < times[1] and times[0] < times[2]):
        print(f"Insertion Sort performed the best for sample size = {n}\n")
    elif (times[1] < times[0] and times[1] < times[2]):
        print(f"Bubble Sort performed the best for sample size = {n}\n")
    elif (times[2] < times[0] and times[2] < times[1]):
        print(f"Selection Sort performed the best for sample size = {n}\n")