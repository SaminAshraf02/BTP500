import pandas as pd
import matplotlib.pyplot as plt
import time

# --- Part 1: Data Processing and Printing (by Jungho Lee) ---

class Node:
    def __init__(self, data):
        self.data = data  # store data
        self.next = None  # pointer to the next node
        self.prev = None  # pointer to the previous node

class DoublyLinkedList:
    def __init__(self):
        self.head = None  # initialize the head as None
        self.tail = None  # initialize the tail as None

    # Insert at front function
    def insert_front(self, data):
        new_node = Node(data)  # create a new node with the data
        if self.head is None:  # if the list is empty
            self.head = self.tail = new_node  # set both head and tail to the new node
        else:  # if the list is not empty
            new_node.next = self.head  # point the new node's next to the current head
            self.head.prev = new_node  # point the current head's previous to the new node
            self.head = new_node  # update the head to be the new node

    # insert at back function
    def insert_back(self, data):
        new_node = Node(data)  # create a new node with the data
        if self.tail is None:  
            self.head = self.tail = new_node  
        else:  
            new_node.prev = self.tail  # point the new node's previous to the current tail
            self.tail.next = new_node  # point the current tail's next to the new node
            self.tail = new_node  # update the tail to be the new node

    # print from head
    def print_head(self, n):
        current = self.head  # start from the head of the list
        count = 0  # a counter so we can stop at the desired number of rows
        while count < n:  # loop until the desired number of rows 
            print(current.data)  # print the data of current node
            current = current.next  # move to the next node
            count += 1  # increment the counter

    # print from tail
    def print_tail(self, n):
        current = self.tail  # start from the tail of the list
        count = 0  # create counter
        while count < n:  # loop until the desired number of rows
            print(current.data)  # print the data of current node backwards
            current = current.prev  # move to the previous node
            count += 1  # increment the counter

# loading file
file_path = r"/Users/saminashraf/Downloads/OntarioCovidLTC.csv"
csv_file = pd.read_csv(file_path, nrows=200)  # load only the first 200 rows of the CSV file

# convert data into dictionary
data_list = []  # initialize an empty list to store rows as dictionaries
columns = csv_file.columns  # get the column names from the file

for row in csv_file.values:  # loop over each row in the file
    row_dict = {}  # initialize an empty dictionary for the current row
    for i in range(len(columns)):  # loop over each column in the row
        row_dict[columns[i]] = row[i]  # assign column name as key and row value as value
    data_list.append(row_dict)  # add the row dictionary to the data_list

# Create Doubly Linked List
dll = DoublyLinkedList()  # initialize an empty doubly linked list
mid = len(data_list) // 2  # find the midpoint of the data_list

# insert the first half of the data in reverse order so that it is inserted in ascending order
for i in range(mid - 1, -1, -1):  # loop from the midpoint-1 to 0 (reverse order)
    dll.insert_front(data_list[i])  # insert each row at the front of the list

# insert the second half of the data in normal order
for i in range(mid, len(data_list)):  # loop from the midpoint to the end of the list
    dll.insert_back(data_list[i])  # insert each row at the back of the list

# Print first 10 rows forward
print("\n-- printing forward --")
dll.print_head(10)  # Print the first 10 rows from the head of the list

# Print last 10 rows backward
print("\n-- printing backward --\n")
dll.print_tail(10)  # Print the last 10 rows from the tail of the list

# --- Part 2: Sorting (by Michael Kidane Melles) ---

# For our example, we choose to sort by the column "Confirmed_Active_LTC_Resident_Cases".
sort_key = "Confirmed_Active_LTC_Resident_Cases"

# Function to plot a bar graph for the first 10 nodes using the chosen key.
def plot_bar_graph(dll, key, title):
    current = dll.head
    x_labels = []
    y_values = []
    count = 0
    while current and count < 10:
        # Use Report_Data_Extracted as x-label if available, otherwise use _id.
        label = current.data.get("Report_Data_Extracted", str(current.data.get("_id", count)))
        x_labels.append(label)
        y_values.append(current.data[key])
        current = current.next
        count += 1
    plt.figure(figsize=(10, 5))
    plt.bar(x_labels, y_values, color='skyblue')
    plt.xlabel("Report Date")
    plt.ylabel(key)
    plt.title(title)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Plot bar graph BEFORE sorting.
plot_bar_graph(dll, sort_key, "Before Sorting: First 10 Rows by " + sort_key)

# Merge Sort on the Doubly Linked List
def split_list(head):
    """Splits the linked list into two halves and returns the head of the second half."""
    slow = head
    fast = head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next
    mid = slow.next
    slow.next = None  # Break the list
    if mid:
        mid.prev = None
    return mid

def merge_sorted(left, right, key):
    """Merges two sorted linked lists based on the given key."""
    if left is None:
        return right
    if right is None:
        return left

    if left.data[key] <= right.data[key]:
        result = left
        result.next = merge_sorted(left.next, right, key)
        if result.next:
            result.next.prev = result
        result.prev = None
    else:
        result = right
        result.next = merge_sorted(left, right.next, key)
        if result.next:
            result.next.prev = result
        result.prev = None
    return result

def merge_sort(head, key):
    """Recursively applies merge sort on the linked list based on the given key."""
    if head is None or head.next is None:
        return head
    second = split_list(head)
    left = merge_sort(head, key)
    right = merge_sort(second, key)
    return merge_sorted(left, right, key)

# Apply merge sort on the linked list.
sorted_head = merge_sort(dll.head, sort_key)
dll.head = sorted_head

# Update dll.tail by traversing from the new head.
current = dll.head
while current.next:
    current = current.next
dll.tail = current

# Plot bar graph AFTER sorting.
plot_bar_graph(dll, sort_key, "After Sorting: First 10 Rows by " + sort_key)

# --- Part 3: Searching (by Samin Ashraf)

# Function to retrieve the value at the middle node of the sorted doubly linked-list.
def get_middle(start, end):

    # Edge case
    if start is None:   # If the list is empty, None is returned

        return None
    
    # The slow-moving pointer moves one step at a time
    slow = start    # Slow-moving pointer is assigned to the beginning node of the sorted doubly-linked list
    # The fast-moving pointer moves two steps at a time
    fast = start    # Fast-moving pointer is assigned to the beginning node of the sorted doubly-linked list

    while fast != end and fast.next != end:     # While loop to move the pointers

        fast = fast.next.next if fast.next and fast.next.next != end else None
        slow = slow.next

        # The loop will continue until:
        #   1. The fast pointer reaches the end of the list
        #   2. The fast pointer reaches the second-to-last node of the list

        # If the fast pointer reaches the end, the loop terminates to prevent unnecessary iterations
        if fast is None:

            break

    # By the time the fast pointer has reached the end, the slow pointer has moved to the middle node
    return slow

# Function for performing binary search on a sorted doubly linked-list
def binary_search_linked_list(start, end, key, target):

    # Edge case
    # Making sure the provided start node argument is not equal to the end node argument
    while start != end:

        # Middle node is provided by the above function get_middle(start, end)
        mid = get_middle(start, end)

        # Edge case, if the sorted doubly linked-list is empty, None is returned
        if mid is None:

            return None
        
        # The middle node's value is retrieved
        mid_value = mid.data[key]

        # If the middle node's value is equal to the target, return the middle node
        if mid_value == target:

            return mid
        
        # If the target value is greater than the middle value, start pointer starts from the head of the sorted doubly linked-list
        elif mid_value < target:

            start = mid.next

        # Otherwise, the target value is searched in the left half of the sorted doubly linked-list
        else:

            end = mid

    return None

# Perform binary search for a successful search and calculate the time taken
# For this example, we are searching for the value 2751 in the "Confirmed_Active_LTC_Resident_Cases" column
# Note: Any value can be used as long as it exists in the column for the search to be successful
target_success = 2751
start_time = time.perf_counter_ns() # Start time
found_node = binary_search_linked_list(dll.head, None, sort_key, target_success)    # Found node containing the target value

# Only works if found_node != None
if found_node:

    print("\nSuccessful Binary Search for target:", target_success)
    print(found_node.data)

# Since we want a successful search and are searching for a value for the search to be successful, the else part will not be executed
else:

    print("\nUnsuccessful Binary Search for target", target_success)

end_time = time.perf_counter_ns()   # End time
print("\nTime taken for successful binary search:", end_time - start_time, "nanoseconds")

# Perform binary search for an unsuccessful search and calculate the time taken
# For this example, we are searching for the value -999 in the "Confirmed_Active_LTC_Resident_Cases" column
# Note: Any value can be used as long as it does not exist in the column for the search to be unsuccessful
target_failure = -999   # Since it is a negative value, it is impossible for it to exist in this column unless due to an error
start_time = time.perf_counter_ns() # Start time
not_found_node = binary_search_linked_list(dll.head, None, sort_key, target_failure)    # None node

# Only works if not_found_node != None
# Since we want an unsuccessful search, the if part will not be executed
if not_found_node:

    print("\nBinary Search (unexpectedly) found:")
    print(not_found_node.data)

# The else part will be executed since no node will be found containing the non-existent target value and not_found_node = None
else:

    print("\nBinary Search unsuccessful for target", target_failure)

end_time = time.perf_counter_ns()   # End timer
print("\nTime taken for unsuccessful binary search:", end_time - start_time, "nanoseconds")