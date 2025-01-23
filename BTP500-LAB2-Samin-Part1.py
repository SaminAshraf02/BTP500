import time
import random

print("\nCourse code: BTP500 Data Structures and Algorithms")
print("Student name: Samin Ashraf")
print("Student ID: 140362229\n")

# Function to create a sorted list of random integers of size n
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

    left_index = 0
    right_index = len(my_list) - 1

    while left_index <= right_index:

        mid_index = (left_index + right_index) // 2

        if key == my_list[mid_index]:

            return mid_index
        
        elif key < my_list[mid_index]:

            right_index = mid_index - 1

        else:

            left_index = mid_index + 1

    return -1

def binary_search_recursive(my_list, key, low_index, high_index):

    if low_index > high_index:
        return -1

    mid_index = (low_index + high_index) // 2

    if key == my_list[mid_index]:

        return mid_index
    
    elif key < my_list[mid_index]:

        return binary_search_recursive(my_list, key, low_index, mid_index - 1)
    
    else:

        return binary_search_recursive(my_list, key, mid_index + 1, high_index)
    
# Test cases
j = 0

while j <= 2:
    
    sample_size = [10, 20, 30]
    times = []
    n = sample_size[j]
    j += 1
    failsafe = 1
    sorted_int_list = sorted_list_creator(n)
    count = 0

    while failsafe == 1:

        start_time = time.perf_counter()

        if (linear_search(sorted_int_list, 1) != -1):

            failsafe = 0

        end_time = time.perf_counter()
        time_taken = end_time - start_time
        times.append(time_taken)
        count += 1

        if (count > 5):

            sorted_int_list[len(sorted_int_list) - 1] = 1
            count = 0

    print(f"Successful Linear Search for sample size = {n}, time taken = {time_taken} seconds")
    failsafe = 1

    while failsafe == 1:

        start_time = time.perf_counter()

        if (linear_search(sorted_int_list, 200) == -1):

            failsafe = 0

        end_time = time.perf_counter()
        time_taken = end_time - start_time
        times.append(time_taken)

    print(f"Unsuccessful Linear Search for sample size = {n}, time taken = {time_taken} seconds\n")
    failsafe = 1

    while failsafe == 1:

        start_time = time.perf_counter()

        if (binary_search(sorted_int_list, 5) != -1):

            failsafe = 0

        end_time = time.perf_counter()
        time_taken = end_time - start_time
        times.append(time_taken)

        count += 1

        if (count > 2):

            sorted_int_list[0] = 5
            count = 0

    print(f"Successful Binary Search for sample size = {n}, time taken = {time_taken} seconds")
    failsafe = 1

    while failsafe == 1:

        start_time = time.perf_counter()

        if (binary_search(sorted_int_list, 200) == -1):

            failsafe = 0

        end_time = time.perf_counter()
        time_taken = end_time - start_time
        times.append(time_taken)

    print(f"Unsuccessful Binary Search for sample size = {n}, time taken = {time_taken} seconds\n")
    failsafe = 1

    while failsafe == 1:

        start_time = time.perf_counter()

        if (binary_search_recursive(sorted_int_list, 5, 0, len(sorted_int_list) - 1) != -1):

            failsafe = 0

        end_time = time.perf_counter()
        time_taken = end_time - start_time
        times.append(time_taken)

    print(f"Successful Binary Search (Recursive) for sample size = {n}, time taken = {time_taken} seconds")
    failsafe = 1

    while failsafe == 1:

        start_time = time.perf_counter()

        if (binary_search_recursive(sorted_int_list, 200, 0, len(sorted_int_list) - 1) == -1):

            failsafe = 0

        end_time = time.perf_counter()
        time_taken = end_time - start_time
        times.append(time_taken)

    print(f"Unsuccessful Binary Search (Recursive) for sample size = {n}, time taken = {time_taken} seconds\n")
    failsafe = 0

    if (times[0] < times[1] and times[0] < times[2]):
        print(f"Linear Search performed the best for sample size = {n}\n")
    elif (times[1] < times[0] and times[1] < times[2]):
        print(f"Binary Search performed the best for sample size = {n}\n")
    elif (times[2] < times[0] and times[2] < times[1]):
        print(f"Binary Search (Recursive) performed the best for sample size = {n}\n")