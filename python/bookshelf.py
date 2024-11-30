import json
import os
import random

class Bookshelf:
    """A class to manage a bookshelf with books."""
    
    def __init__(self, file_name="bookshelf.json"):
        self.file_name = file_name
        self.books = self.load_bookshelf()

    def load_bookshelf(self):
        """Loads the bookshelf from a JSON file or creates a new one."""
        if os.path.exists(self.file_name):
            with open(self.file_name, "r") as file:
                return json.load(file)
        return []

    def save_bookshelf(self):
        """Saves the bookshelf to a JSON file."""
        with open(self.file_name, "w") as file:
            json.dump(self.books, file, indent=4)

    def add_book(self, title, author, genre):
        """Adds a new book to the bookshelf."""
        book = {
            "title": title,
            "author": author,
            "genre": genre,
            "rating": random.randint(1, 5)  # Random rating for fun
        }
        self.books.append(book)
        self.save_bookshelf()
        print(f"Book '{title}' added successfully!")

    def show_bookshelf(self):
        """Displays all books on the bookshelf."""
        if not self.books:
            print("\nYour bookshelf is empty.")
            return
        
        print("\nYour Bookshelf:")
        for i, book in enumerate(self.books, start=1):
            print(f"\nBook {i}:")
            print(f"  Title : {book['title']}")
            print(f"  Author: {book['author']}")
            print(f"  Genre : {book['genre']}")
            print(f"  Rating: {'⭐' * book['rating']} ({book['rating']}/5)")

    def search_books(self, keyword):
        """Searches for books by title or author."""
        matches = [
            book for book in self.books
            if keyword.lower() in book['title'].lower() or keyword.lower() in book['author'].lower()
        ]
        if matches:
            print("\nSearch Results:")
            for book in matches:
                print(f"  - {book['title']} by {book['author']} (Genre: {book['genre']})")
        else:
            print("No matches found!")

    def recommend_book(self):
        """Recommends a random book from the bookshelf."""
        if not self.books:
            print("\nNo books to recommend! Add some first.")
            return
        book = random.choice(self.books)
        print("\nRecommendation:")
        print(f"  Title : {book['title']}")
        print(f"  Author: {book['author']}")
        print(f"  Genre : {book['genre']}")
        print(f"  Rating: {'⭐' * book['rating']} ({book['rating']}/5)")


# Main Program
if __name__ == "__main__":
    bookshelf = Bookshelf()

    while True:
        print("\nBookshelf Manager")
        print("1. Add a Book")
        print("2. Show Bookshelf")
        print("3. Search Books")
        print("4. Recommend a Book")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            genre = input("Enter book genre: ")
            bookshelf.add_book(title, author, genre)

        elif choice == "2":
            bookshelf.show_bookshelf()

        elif choice == "3":
            keyword = input("Enter a keyword to search: ")
            bookshelf.search_books(keyword)

        elif choice == "4":
            bookshelf.recommend_book()

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")