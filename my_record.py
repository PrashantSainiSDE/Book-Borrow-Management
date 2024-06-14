import sys

class Book:
    def __init__(self, book_id, name, book_type, num_copies, max_days, late_charge):
        self.book_id = book_id
        self.name = name
        self.book_type = book_type
        self.num_copies = num_copies
        self.max_days = max_days
        self.late_charge = late_charge
        self.borrowed_days = {}

    def add_borrowed_days(self, member_id, days):
        self.borrowed_days[member_id] = days
    
    def num_borrowing_members(self):
        return sum(1 for days in self.borrowed_days.values() if days.isdigit())

    def num_reserving_members(self):
        return sum(1 for days in self.borrowed_days.values() if days == 'R')

    def range_of_borrowing_days(self):
        days = [int(d) for d in self.borrowed_days.values() if d.isdigit()]
        return (min(days), max(days)) if days else (0, 0)

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
                        self.books[book_id] = Book(book_id, "", "", 0, 0, 0.0)

                    for part in parts[1:]:
                        member_id, days = part.split(': ')
                        if member_id not in self.members:
                            self.members[member_id] = Member(member_id)
                        
                        self.books[book_id].add_borrowed_days(member_id, days)
                        self.members[member_id].add_borrowed_book(book_id, days)
        except FileNotFoundError:
            print(f"Error: The file {record_file_name} does not exist.")
            sys.exit(1)

    def read_books(self, book_file_name):
        try:
            with open(book_file_name, 'r') as file:
                for line in file:
                    parts = line.strip().split(', ')
                    book_id, name, book_type, num_copies, max_days, late_charge = parts
                    num_copies = int(num_copies)
                    max_days = int(max_days)
                    late_charge = float(late_charge)

                    if book_type == 'T' and max_days != 14:
                        print(f"Error: Textbook {book_id} must have a max borrowing days of 14.")
                        return False
                    if book_type == 'F' and max_days <= 14:
                        print(f"Error: Fiction book {book_id} must have a max borrowing days greater than 14.")
                        return False

                    self.books[book_id].name = name
                    self.books[book_id].book_type = book_type
                    self.books[book_id].num_copies =  num_copies
                    self.books[book_id].max_days = max_days
                    self.books[book_id].late_charge = late_charge

        except FileNotFoundError:
            print(f"Error: The file {book_file_name} does not exist.")
            sys.exit(1)

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

    def display_books(self):
        print("\nBOOK INFORMATION")
        print("-" * 110)
        print(f"| {'Book IDs':<10} {'Name':<15} {'Type':<15} {'Ncopy':<10} {'Maxday':<10} {'Lcharge':<10} {'Nborrow':<10} {'Nreserve':<10} {'Range':<8} |")
        print("-" * 110)

        for book in self.books.values():
            book_type = "Textbook" if book.book_type == 'T' else "Fiction"
            nborrow = book.num_borrowing_members()
            nreserve = book.num_reserving_members()
            min_days, max_days = book.range_of_borrowing_days()

            print(f"| {book.book_id:<10} {book.name:<15} {book_type:<18} {book.num_copies:<10} {book.max_days:<10} {book.late_charge:<12.1f} {nborrow:<12} {nreserve:<4} {min_days}-{max_days:<5} |")

        print("-" * 110)

        print("BOOK SUMMARY")
        most_popular_books = sorted(self.books.values(), key=lambda b: b.num_borrowing_members() + b.num_reserving_members(), reverse=True)
        most_popular_book = most_popular_books[0]
        print(f"The most popular book is {most_popular_book.name}.")

        # Determine the book with the longest days borrowed
        longest_borrowed_books = sorted(self.books.values(), key=lambda b: b.range_of_borrowing_days()[1], reverse=True)
        longest_borrowed_book = longest_borrowed_books[0]
        print(f"The book {longest_borrowed_book.name} has the longest borrow days ({longest_borrowed_book.range_of_borrowing_days()[1]} days).")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("[Usage:] python my_record.py <record_file> [<book_file>]")
    else:
        records = Records()
        records.read_records(sys.argv[1])
        
        if(len(sys.argv) == 3):
             records.read_books(sys.argv[2])
        
        records.display_records()

        if(len(sys.argv) == 3):
             records.display_books()
