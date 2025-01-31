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

# Function to perform merge sort
def merge_sort(mylist):

    empty_list = [0] * len(mylist)

    recursive_merge_sort(mylist, 0, len(mylist) - 1, empty_list)

# Recursive merge sort function
def recursive_merge_sort(mylist, first_index, last_index, empty_list):

    if first_index < last_index:

        mid_index = (first_index + last_index) // 2

        recursive_merge_sort(mylist, first_index, mid_index, empty_list)
        recursive_merge_sort(mylist, mid_index + 1, last_index, empty_list)

        merge(mylist, first_index, mid_index + 1, last_index, empty_list)

# Function to merge the sorted lists
def merge(mylist, a_first_index, b_first_index, b_last_index, empty_list):

    a_ptr = a_first_index
    b_ptr = b_first_index
    empty_list_index = a_ptr

    while (a_ptr < b_first_index) and (b_ptr <= b_last_index):

        if mylist[a_ptr] <= mylist[b_ptr]:

            empty_list[empty_list_index] = mylist[a_ptr]
            empty_list_index += 1
            a_ptr += 1

        else:

            empty_list[empty_list_index] = mylist[b_ptr]
            empty_list_index += 1
            b_ptr += 1

    while a_ptr < b_first_index:

        empty_list[empty_list_index] = mylist[a_ptr]
        empty_list_index += 1
        a_ptr += 1

    while b_ptr <= b_last_index:

        empty_list[empty_list_index] = mylist[b_ptr]
        empty_list_index += 1
        b_ptr += 1

    for i in range(a_first_index, b_last_index + 1):

        mylist[i] = empty_list[i]

# Function to perform quick sort
def quick_sort(mylist):

    recursive_quick_sort(mylist, 0, len(mylist) - 1)

# Recursive quick sort function
def recursive_quick_sort(mylist, left, right, THRESHOLD=32):

    if right - left <= THRESHOLD:

        insertion_sort(mylist, left, right)

    else:

        pivot_position = partition(mylist, left, right)
        recursive_quick_sort(mylist, left, pivot_position - 1)
        recursive_quick_sort(mylist, pivot_position + 1, right)

# Insertion sort function used by the recursive quick sort function
def insertion_sort(mylist, left, right):

    for i in range(left + 1, right + 1):

        curr = mylist[i]
        j = i

        while j > left and mylist[j - 1] > curr:

            mylist[j] = mylist[j - 1]
            j = j - 1

        mylist[j] = curr

# Function to divide the list into halves
def partition(mylist, left, right):

    pivot_location = random.randint(left, right)

    pivot = mylist[pivot_location]

    mylist[pivot_location] = mylist[right]
    mylist[right] = pivot

    end_of_smaller = left - 1

    for j in range(left, right):

        if mylist[j] <= pivot:

            end_of_smaller += 1
            mylist[end_of_smaller], mylist[j] = mylist[j], mylist[end_of_smaller]

    mylist[end_of_smaller + 1], mylist[right] = mylist[right], mylist[end_of_smaller + 1]

    return end_of_smaller + 1

# Test cases
i = 0
test_cases = [50, 500, 700]
times = []

for i in test_cases:
    n = i

    list_to_sort = array_creator(n)
    list_to_sort1 = array_creator(n)

    start_time = time.perf_counter()

    merge_sort(list_to_sort)

    end_time = time.perf_counter()

    times.append(end_time - start_time)

    start_time = time.perf_counter()

    quick_sort(list_to_sort1)

    end_time = time.perf_counter()

    times.append(end_time - start_time)


    if (times[0] < times[1]):

        print(f"Merge Sort performed the best for sample size = {n}\n")

    elif (times[1] < times[0]):

        print(f"Quick Sort performed the best for sample size = {n}\n")