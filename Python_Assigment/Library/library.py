from datetime import datetime, timedelta
from typing import List, Optional


class Book:
    """
    A class representing a book in the library.
    
    Attributes:
        title (str): Title of the book
        author (str): Author of the book
        isbn (str): International Standard Book Number
        available (bool): Availability status
    """
    
    def __init__(self, title: str, author: str, isbn: str):
        """
        Initialize Book instance.
        
        Args:
            title (str): Book title
            author (str): Book author
            isbn (str): Unique ISBN identifier
        """
        self.title = title
        self.author = author
        self.isbn = isbn
        self.available = True
        self.borrowed_by: Optional['Member'] = None
        self.due_date: Optional[datetime] = None
    
    def borrow(self, member: 'Member') -> bool:
        """
        Mark book as borrowed by a member.
        
        Args:
            member (Member): Member borrowing the book
            
        Returns:
            bool: True if successful, False if book is unavailable
        """
        if self.available:
            self.available = False
            self.borrowed_by = member
            self.due_date = datetime.now() + timedelta(days=14)  # 2 weeks loan
            return True
        return False
    
    def return_book(self) -> bool:
        """
        Mark book as returned.
        
        Returns:
            bool: True if successful, False if book wasn't borrowed
        """
        if not self.available:
            self.available = True
            self.borrowed_by = None
            self.due_date = None
            return True
        return False
    
    def is_overdue(self) -> bool:
        """Check if book is overdue."""
        if self.due_date and datetime.now() > self.due_date:
            return True
        return False
    
    def __str__(self) -> str:
        """String representation of Book."""
        status = "Available" if self.available else f"Borrowed by {self.borrowed_by.name}"
        return f"Book('{self.title}', '{self.author}', {status})"


class Member:
    """
    A class representing a library member.
    
    Attributes:
        name (str): Member's name
        member_id (str): Unique member identifier
        borrowed_books (List[Book]): List of currently borrowed books
    """
    
    def __init__(self, name: str, member_id: str):
        """
        Initialize Member instance.
        
        Args:
            name (str): Member's full name
            member_id (str): Unique member ID
        """
        self.name = name
        self.member_id = member_id
        self.borrowed_books: List[Book] = []
    
    def borrow_book(self, book: Book) -> str:
        """
        Borrow a book from the library.
        
        Args:
            book (Book): Book to borrow
            
        Returns:
            str: Result message
        """
        if len(self.borrowed_books) >= 5:  # Limit of 5 books per member
            return "Cannot borrow more than 5 books"
        
        if book.borrow(self):
            self.borrowed_books.append(book)
            return f"Successfully borrowed '{book.title}'"
        else:
            return f"Book '{book.title}' is not available"
    
    def return_book(self, book: Book) -> str:
        """
        Return a borrowed book.
        
        Args:
            book (Book): Book to return
            
        Returns:
            str: Result message
        """
        if book in self.borrowed_books:
            book.return_book()
            self.borrowed_books.remove(book)
            
            if book.is_overdue():
                return f"Book '{book.title}' returned (OVERDUE!)"
            else:
                return f"Book '{book.title}' returned successfully"
        else:
            return "This book was not borrowed by you"
    
    def get_borrowed_books(self) -> List[str]:
        """Get list of borrowed book titles."""
        return [book.title for book in self.borrowed_books]
    
    def __str__(self) -> str:
        """String representation of Member."""
        return f"Member('{self.name}', ID: {self.member_id}, Books: {len(self.borrowed_books)})"


class Library:
    """
    A class representing a library with books and members.
    
    Attributes:
        name (str): Library name
        books (List[Book]): Collection of books
        members (List[Member]): Registered members
    """
    
    def __init__(self, name: str):
        """Initialize Library with name."""
        self.name = name
        self.books: List[Book] = []
        self.members: List[Member] = []
    
    def add_book(self, book: Book) -> None:
        """Add a book to the library collection."""
        self.books.append(book)
    
    def add_member(self, member: Member) -> None:
        """Register a new member."""
        self.members.append(member)
    
    def find_book(self, title: str) -> Optional[Book]:
        """Find a book by title."""
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None
    
    def find_member(self, member_id: str) -> Optional[Member]:
        """Find a member by ID."""
        for member in self.members:
            if member.member_id == member_id:
                return member
        return None
    
    def get_available_books(self) -> List[Book]:
        """Get list of available books."""
        return [book for book in self.books if book.available]
    
    def get_borrowed_books(self) -> List[Book]:
        """Get list of borrowed books."""
        return [book for book in self.books if not book.available]
    
    def display_books(self) -> None:
        """Display all books with their status."""
        print(f"\n--- Books in {self.name} Library ---")
        for book in self.books:
            status = "Available" if book.available else f"Borrowed (Due: {book.due_date.strftime('%Y-%m-%d')})"
            print(f"  - {book.title} by {book.author} [{status}]")


# Demonstration
if __name__ == "__main__":
    # Create library
    library = Library("City Central Library")
    
    # Add books
    books_data = [
        ("The Great Gatsby", "F. Scott Fitzgerald", "978-0-7432-7356-5"),
        ("To Kill a Mockingbird", "Harper Lee", "978-0-06-112008-4"),
        ("1984", "George Orwell", "978-0-452-28423-4"),
        ("Pride and Prejudice", "Jane Austen", "978-0-14-143951-8")
    ]
    
    for title, author, isbn in books_data:
        library.add_book(Book(title, author, isbn))
    
    # Add members
    member1 = Member("Alice Johnson", "M001")
    member2 = Member("Bob Smith", "M002")
    library.add_member(member1)
    library.add_member(member2)
    
    # Demonstrate operations
    print("=== Library Management System Demo ===")
    library.display_books()
    
    # Borrow books
    print(f"\n--- Borrowing Books ---")
    book1 = library.find_book("The Great Gatsby")
    book2 = library.find_book("1984")
    
    if book1:
        print(member1.borrow_book(book1))
    if book2:
        print(member1.borrow_book(book2))
    
    library.display_books()
    
    # Return book
    print(f"\n--- Returning Books ---")
    if book1:
        print(member1.return_book(book1))
    
    library.display_books()