#starter Code
import time

# Counter for operations
iterative_operations = 0
recursive_operations = 0

# Iterative factorial function
def factorial_iterative(n):
    result = 1
    while n >= 1:
        result *= n
        n -= 1
    return result

# Recursive factorial function
def factorial_recursive(n):
    result = 1                                     # 1
    if (n > 1):                                    # 1
        result = n * factorial_recursive(n-1)      # 3 + number of operations done by factorial_recursive(n-1)
    return result                                  # 1

# Function to measure time and compare
def compare_factorial_methods(n):
   
    # Measure iterative factorial time
    start_time_ns_iterative = time.perf_counter_ns()
    result1 = factorial_iterative(n)
    end_time_ns_iterative = time.perf_counter_ns()
   
    # Measure recursive factorial time
    start_time_ns_recursive = time.perf_counter_ns()   
    result2 = factorial_recursive(n)
    end_time_ns_recursive = time.perf_counter_ns()

    # Time calculations
    time_taken_ns_iterative = end_time_ns_iterative - start_time_ns_iterative
    time_taken_ns_recursive = end_time_ns_recursive - start_time_ns_recursive
    
    print(f"Factorial of {n} (Iterative): {result1}, Time taken: {time_taken_ns_iterative} nanoseconds, Operators used (Iterative): {n}")
    print(f"Factorial of {n} (Recursive): {result2}, Time taken: {time_taken_ns_recursive} nanoseconds, Operators used (Recursive): {n-1}")
    
# Tester 1
n = 5  
print(f"Tester 1: n={n}")
compare_factorial_methods(n)

# Tester 2
n = 10  
print(f"Tester 2: n={n}")
compare_factorial_methods(n)

# Tester 3
n = 15  
print(f"Tester 3: n={n}")
compare_factorial_methods(n)