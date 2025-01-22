import time
import random

print("Course code: BTP500 Data Structures and Algorithms")
print("Student name: Samin Ashraf")
print("Student ID: 140362229\n")

def array_creator(n):
    i = 0
    int_array = []

    while n > 0 and i < n:
        i += 1
        generated_random_integer = random.randint(1, 100)
        int_array.append(generated_random_integer)

    return int_array

def insertion_sort(my_list):
    for i in range(1, len(my_list)):
        curr = my_list[i]  # store the first number in the unsorted part of
                           # of array into curr
        j = i
        while j > 0 and my_list[j - 1] > curr:       # this loop shifts value within sorted part of array
            my_list[j] = my_list[j - 1]              # to open a spot for curr
            j -= 1
        my_list[j] = curr

def bubble_sort(my_list):
    n = len(my_list)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if my_list[j] > my_list[j + 1]:
                my_list[j], my_list[j + 1] = my_list[j + 1], my_list[j]

def selection_sort(my_list):

    n = len(my_list)
    for i in range(n - 1):
        min_idx = i  # record the index of the smallest value,
                     # initialized with where the smallest value may be found
        for j in range(i + 1, n):              # go through list, 
            if my_list[j] < my_list[min_idx]:  # and every time we find a smaller value,
                min_idx = j                    # record its index (note how nothing has moved at this point.)


        if min_idx != i:
            my_list[min_idx], my_list[i] = my_list[i], my_list[min_idx]

# Test cases
j = 0
while j <= 2:
    sample_size = [100, 200, 300]
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
    print(f"Sample size = {n}, Algorithm = Insertion Sort, Time taken = {time_taken} second(s)")

    start_time = time.perf_counter()
    bubble_sort(bubble_sort_array)
    end_time = time.perf_counter()
    time_taken = end_time - start_time
    print(f"Sample size = {n}, Algorithm = Bubble Sort,    Time taken = {time_taken} second(s)")

    start_time = time.perf_counter()
    selection_sort(selection_sort_array)
    end_time = time.perf_counter()
    time_taken = end_time - start_time
    print(f"Sample size = {n}, Algorithm = Selection Sort, Time taken = {time_taken} second(s)\n")
