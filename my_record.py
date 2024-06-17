import sys
import datetime

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
    def __init__(self, member_id, first_name, last_name, dob, member_type):
        self.member_id = member_id
        self.first_name = first_name
        self.last_name = last_name
        self.dob = dob
        self.member_type = member_type
        self.borrowed_books = {}

    def add_borrowed_book(self, book_id, days):
        self.borrowed_books[book_id] = days
        
    def num_textbooks(self, books):
        return sum(1 for book_id in self.borrowed_books.keys() if books[book_id].book_type == 'T')

    def num_fictions(self, books):
        return sum(1 for book_id in self.borrowed_books.keys() if books[book_id].book_type == 'F')

    def average_borrow_days(self):
        days = [int(d) for d in self.borrowed_books.values() if d.isdigit()]
        return sum(days) / len(days)

    def validate_borrowing_limits(self, num_textbooks, num_fictions):
        if self.member_type == "Standard":
            return num_textbooks <= 1 and num_fictions <= 2
        elif self.member_type == "Premium":
            return num_textbooks <= 2 and num_fictions <= 3

    def validate_reserving_limits(self, books):
        num_textbooks = sum(1 for book_id, days in self.borrowed_books.items() if days == 'R' and books[book_id].book_type == 'T')
        num_fictions = sum(1 for book_id, days in self.borrowed_books.items() if days == 'R' and books[book_id].book_type == 'F')
        if self.member_type == "Standard":
            return num_textbooks <= 1 and num_fictions <= 2
        elif self.member_type == "Premium":
            return num_textbooks <= 2 and num_fictions <= 3
        
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
                            self.members[member_id] = Member(member_id, "", "", "", "")
                        
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

    def read_members(self, member_file_name):
        try:
            with open(member_file_name, 'r') as file:
                for line in file:
                    parts = line.strip().split(', ')
                    if(len(parts) == 5):
                        member_id, first_name, last_name, dob, member_type = parts
                   
                        self.members[member_id].first_name = first_name
                        self.members[member_id].last_name = last_name
                        self.members[member_id].dob = dob
                        self.members[member_id].member_type = member_type

        except FileNotFoundError:
            print(f"Error: The file {member_file_name} does not exist.")

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

    def display_members(self):
        print("\nMEMBER INFORMATION")
        print("-" * 101)
        print(f"| {'Member IDs':<15} {'FName':<10} {'LName':<5} {'Type':>15} {'DOB':>15} {'Ntextbook':>10} {'Nfiction':>10} {'Average':>10} |")
        print("-" * 101)

        most_active_member = None
        most_books_borrowed = 0
        least_avg_days_member = None
        least_avg_days = float('inf')
        sorted_members = sorted(self.members)

        for member in sorted_members:
            ntextbooks = self.members[member].num_textbooks(self.books)
            nfictions = self.members[member].num_fictions(self.books)
            avg_days = self.members[member].average_borrow_days()
            ntextbooks_str = f"{ntextbooks}!" if not self.members[member].validate_borrowing_limits(ntextbooks, nfictions) else str(ntextbooks)
            nfictions_str = f"{nfictions}!" if not self.members[member].validate_reserving_limits(self.books) else str(nfictions)
            
            dob = datetime.datetime.strptime(self.members[member].dob, "%m/%d/%Y").strftime("%d-%b-%Y")

            print(f"| {self.members[member].member_id:<15} {self.members[member].first_name:<10} {self.members[member].last_name:<10} {self.members[member].member_type:>10} {dob:>15} {ntextbooks_str:>10} {nfictions_str:>10} {avg_days:>10.2f} |")

            total_borrowed = ntextbooks + nfictions
            if total_borrowed > most_books_borrowed:
                most_books_borrowed = total_borrowed
                most_active_member = self.members[member]

            if avg_days < least_avg_days:
                least_avg_days = avg_days
                least_avg_days_member = self.members[member]

        print("-" * 101)

        print("MEMBER SUMMARY")
        print(f"The most active member is: {most_active_member.first_name} {most_active_member.last_name} with {most_books_borrowed} books borrowed/reserved.")
        print(f"The member with the least average number of borrowing days is {least_avg_days_member.first_name} {least_avg_days_member.last_name} with {least_avg_days:.2f} days.")
  
    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            pass

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("[Usage:] python my_record.py <record_file> [<book_file>] [<member_file>]")
    else:
        records = Records()
        records.read_records(sys.argv[1])
        records.display_records()
        
        if(len(sys.argv) > 2):
             records.read_books(sys.argv[2])
             records.display_books()
        
        if(len(sys.argv) > 3):
             records.read_members(sys.argv[3])
             records.display_members()
