print("\nCourse code: BTP500 Data Structures and Algorithms")
print("Student name: Samin Ashraf")
print("Student ID: 140362229\n")

class HashTable:

    def __init__(self, size):

        self.size = size
        self.table = [None] * size

    def _hash(self, key):

        return hash(key) % self.size

    def insert(self, key, value):

        index = self._hash(key)

        if self.table[index] is None:

            self.table[index] = [(key, value)]

        else:


            for i, (existing_key, _) in enumerate(self.table[index]):

                if existing_key == key:

                    self.table[index][i] = (key, value)
                    return

            self.table[index].append((key, value))

    def delete(self, key):

        index = self._hash(key)

        if self.table[index] is not None:

            for i, (existing_key, _) in enumerate(self.table[index]):

                if existing_key == key:

                    del self.table[index][i]

                    if not self.table[index]:

                        self.table[index] = None

                    return True

        return False

    def update(self, key, new_value):

        index = self._hash(key)

        if self.table[index] is not None:

            for i, (existing_key, _) in enumerate(self.table[index]):

                if existing_key == key:

                    self.table[index][i] = (key, new_value)
                    return True

        return False

    def find(self, key):

        index = self._hash(key)

        if self.table[index] is not None:

            for existing_key, value in self.table[index]:

                if existing_key == key:

                    return value

        return None

    def enumerate(self):

        for i in range(self.size):

            if self.table[i] is not None:

                for key, value in self.table[i]:

                    print(f"Index {i}: {key} -> {value}")

# Demonstration
# Initialize the hash table
hash_table = HashTable(6)

# Inserting directors
hash_table.insert("Rob Minkoff", "Director")
hash_table.insert("Bill Condon", "Director")
hash_table.insert("Josh Cooley", "Director")
hash_table.insert("Brad Bird", "Director")
hash_table.insert("Lake Bell", "Director")

# Inserting movie titles
hash_table.insert("The Lion King", "Movie Title")
hash_table.insert("Beauty and the Beast", "Movie Title")
hash_table.insert("Toy Story 4", "Movie Title")
hash_table.insert("Mission Impossible", "Movie Title")
hash_table.insert("The Secret Life of Pets", "Movie Title")

# Inserting release years
hash_table.insert(2019, "Release Year")
hash_table.insert(2017, "Release Year")
hash_table.insert(2019, "Release Year")
hash_table.insert(2018, "Release Year")
hash_table.insert(2016, "Release Year")

# Inserting scores
hash_table.insert(3.50, "Score")
hash_table.insert(4.20, "Score")
hash_table.insert(4.50, "Score")
hash_table.insert(5.00, "Score")
hash_table.insert(3.90, "Score")

# Display the hash table after insertion
print("Hash Table after insertion:")
hash_table.enumerate()

# Delete operations
hash_table.delete("The Secret Life of Pets")
hash_table.delete(3.90)
hash_table.delete(2016)
hash_table.delete("Lake Bell")

# Display the hash table after deletion
print("\nHash Table after deletion:")
hash_table.enumerate()

# Update operations
hash_table.update("Toy Story 4", "Toy Story 3")
hash_table.update(2019, 2010)
hash_table.update("Josh Cooley", "Lee Unkrich")
hash_table.update(4.50, 5.00)

# Display the hash table after update
print("\nHash Table after update:")
hash_table.enumerate()

# Find operations
print("\nFind operations:")
print("Mission Impossible:", hash_table.find("Mission Impossible"))
print("Bill Condon:", hash_table.find("Bill Condon"))
print("2018:", hash_table.find(2018))
print("3.50:", hash_table.find(3.50))

# Enumerate all items
print("\nEnumerate all items:")
hash_table.enumerate()