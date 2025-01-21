import time

time_taken = 0

print("Student name: Samin Ashraf")
print("Lab 1")
print("Algorithm name: \n")

def fibonacci_series(n):

    start_time_ns = time.perf_counter_ns()

    # If n is less than or equal to 0, an empty array will be returned
    if n <= 0:
        return []
    # If n is 1, the returned array will only contain 0
    elif n == 1:
        return [0]
    # If n is 2, the returned array will contain 0 and 1
    elif n == 2:
        return [0, 1]

    # Initialize the first two terms
    fib_series = [0, 1]

    # Generate the series
    for i in range(2, n):
        # The next number (sum of the last two numbers) is appended to the end of the array
        fib_series.append(fib_series[-1] + fib_series[-2])

    end_time_ns = time.perf_counter_ns()
    time_taken = end_time_ns - start_time_ns

    # The fibonacci series array is returned
    return fib_series

# Test cases
n = 5
print(f"Fibonacci series ({n} terms) {fibonacci_series(n)}")
print(f"Time taken: {time_taken} ns\n")
n = 17
print(f"Fibonacci series ({n} terms) {fibonacci_series(n)}")
print(f"Time taken: {time_taken} ns\n")
n = 37
print(f"Fibonacci series ({n} terms) {fibonacci_series(n)}")
print(f"Time taken: {time_taken} ns")