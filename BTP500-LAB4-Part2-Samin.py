print("\nCourse code: BTP500 Data Structures and Algorithms")
print("Student name: Samin Ashraf")
print("Student ID: 140362229\n")

# Part 2.1

print("Part 2.1")

class Queue:

    def __init__(self, max_size):

        self.queue = []
        self.max_size = max_size
        self.front = -1
        self.rear = -1

    def enqueue(self, item):

        if self.isFull():

            print("Queue is full. Cannot enqueue more items.")

        else:

            if self.isEmpty():

                self.front = 0

            self.rear += 1
            self.queue.append(item)
            print(f"Enqueued: {item}")

    def dequeue(self):

        if self.isEmpty():

            print("Queue is empty. Cannot dequeue.")
            return None

        else:

            item = self.queue.pop(0)
            self.front += 1

            if self.front > self.rear:

                self.front = -1
                self.rear = -1

            print(f"Dequeued: {item}")
            return item

    def front_element(self):

        if self.isEmpty():

            print("Queue is empty. No front element.")
            return None

        else:

            return self.queue[self.front]

    def back_element(self):

        if self.isEmpty():

            print("Queue is empty. No rear element.")
            return None

        else:

            return self.queue[self.rear]

    def isEmpty(self):

        return self.front == -1 and self.rear == -1

    def isFull(self):

        return self.rear == self.max_size - 1


# Demonstration
queue = Queue(max_size=5)

fruits = ["Apples", "Bananas", "Grapes", "Berries", "Oranges"]

for fruit in fruits:

    queue.enqueue(fruit)

print(f"Is the queue full? {queue.isFull()}")
print(f"Front: {queue.front_element()}")
print(f"Rear: {queue.back_element()}")

queue.dequeue()
queue.dequeue()

print(f"Is the queue empty? {queue.isEmpty()}")

# Part 2.2

print()
print("Part 2.2")

class Queue:

    def __init__(self, max_size):

        self.queue = []
        self.max_size = max_size
        self.front = -1
        self.rear = -1

    def enqueue(self, item):

        if self.isFull():

            print("Queue is full. Cannot enqueue more items.")

        else:

            if self.isEmpty():

                self.front = 0

            self.rear += 1
            self.queue.append(item)
            print(f"Enqueued: {item}")

    def dequeue(self):

        if self.isEmpty():

            print("Queue is empty. Cannot dequeue.")
            return None
        
        else:

            item = self.queue.pop(0)
            self.front += 1

            if self.front > self.rear:

                self.front = -1
                self.rear = -1

            print(f"Dequeued: {item}")
            return item

    def front_element(self):

        if self.isEmpty():

            print("Queue is empty. No front element.")
            return None

        else:

            return self.queue[self.front]

    def back_element(self):

        if self.isEmpty():

            print("Queue is empty. No rear element.")
            return None
        
        else:

            return self.queue[self.rear]

    def isEmpty(self):

        return self.front == -1 and self.rear == -1

    def isFull(self):

        return self.rear == self.max_size - 1


# Main program
if __name__ == "__main__":

    queue = Queue(max_size=5)


    fruits = ["Apples", "Bananas", "Grapes", "Berries", "Oranges"]
    for fruit in fruits:
        queue.enqueue(fruit)


    print(f"Is the queue full? {queue.isFull()}")


    print(f"Front: {queue.front_element()}")
    print(f"Rear: {queue.back_element()}")


    queue.dequeue()
    queue.dequeue()


    print(f"Is the queue empty? {queue.isEmpty()}")