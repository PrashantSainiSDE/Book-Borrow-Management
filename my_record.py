import sys

class Book:
    def __init__(self, book_id):
        self.book_id = book_id
        self.borrowed_days = {}

    def add_borrowed_days(self, member_id, days):
        self.borrowed_days[member_id] = days

class Member:
    def __init__(self, member_id):
        self.member_id = member_id
        self.borrowed_books = {}

    def add_borrowed_book(self, book_id, days):
        self.borrowed_books[book_id] = days

class Records:
    def __init__(self):
        self.books = {}
        self.members = {}

    def read_records(self, record_file_name):
        try:
            with open(record_file_name, 'r') as file:
                for line in file:
                    parts = line.strip().split(', ')
                    book_id = parts[0]
                    if book_id not in self.books:
                        self.books[book_id] = Book(book_id)

                    for part in parts[1:]:
                        member_id, days = part.split(': ')
                        if member_id not in self.members:
                            self.members[member_id] = Member(member_id)
                        
                        self.books[book_id].add_borrowed_days(member_id, days)
                        self.members[member_id].add_borrowed_book(book_id, days)
        except FileNotFoundError:
            print(f"Error: The file {record_file_name} does not exist.")

    def display_records(self):
        print("\nRECORDS")
        print("-" * 64)
        
        books_ids = sorted(self.books.keys())
        print("| Member IDs", end='')
        for book_id in books_ids:
            print(f"{book_id:>10}", end='')
        print(" |")
        print("-" * 64)

        for member_id in self.members.keys():
            print(f"| {member_id:<10}", end='')
            for book_id in books_ids:
                days = self.books[book_id].borrowed_days.get(member_id, 'xx')
                if days == 'R':
                    days = '--'
                print(f"{days:>10}", end='')
            print(" |")
        print("-" * 64)

        print("RECORDS SUMMARY")
        total_books = len(self.books)
        total_members = len(self.members)
        total_days = 0
        num_times_book = 0 
        
        for books in self.members.values():
            for days in books.borrowed_books.values():
                if days.isdigit():
                    total_days += int(days) 
                    num_times_book += 1

        average_days = total_days / num_times_book

        print(f"There are {total_members} members and {total_books} books.")
        print(f"The average number of borrow days is {average_days:.2f} (days).")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("[Usage:] python my_record.py <record_file>")
    else:
        records = Records()
        records.read_records(sys.argv[1])
        records.display_records()
