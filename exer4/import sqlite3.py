import sqlite3

# Function to create the database and tables
def create_database():
    # Connect to the database
    connection = sqlite3.connect('library.db')

    # Create the Books table
    connection.execute('''CREATE TABLE IF NOT EXISTS Books
                         (BookID INTEGER PRIMARY KEY,
                          Title TEXT,
                          Author TEXT,
                          ISBN TEXT,
                          Status TEXT)''')

    # Create the Users table
    connection.execute('''CREATE TABLE IF NOT EXISTS Users
                         (UserID INTEGER PRIMARY KEY,
                          Name TEXT,
                          Email TEXT)''')

    # Create the Reservations table
    connection.execute('''CREATE TABLE IF NOT EXISTS Reservations
                         (ReservationID INTEGER PRIMARY KEY,
                          BookID INTEGER,
                          UserID INTEGER,
                          ReservationDate DATE,
                          FOREIGN KEY (BookID) REFERENCES Books(BookID),
                          FOREIGN KEY (UserID) REFERENCES Users(UserID))''')

    # Commit the changes and close the connection
    connection.commit()
    connection.close()

# Function to add a new book to the database
def add_book():
    # Connect to the database
    connection = sqlite3.connect('library.db')

    # Get input from the user
    title = input("Enter the book title: ")
    author = input("Enter the author: ")
    isbn = input("Enter the ISBN: ")
    status = input("Enter the status: ")

    # Insert the book into the Books table
    connection.execute("INSERT INTO Books (Title, Author, ISBN, Status) VALUES (?, ?, ?, ?)", (title, author, isbn, status))

    # Commit the changes and close the connection
    connection.commit()
    connection.close()

# Function to find a book's details based on BookID
def find_book_details(book_id):
    # Connect to the database
    connection = sqlite3.connect('library.db')

    # Retrieve the book details using JOIN
    cursor = connection.execute('''SELECT Books.BookID, Books.Title, Books.Author, Books.ISBN, Books.Status,
                                     Reservations.UserID, Reservations.ReservationDate,
                                     Users.Name, Users.Email
                                  FROM Books
                                  LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                                  LEFT JOIN Users ON Reservations.UserID = Users.UserID
                                  WHERE Books.BookID = ?''', (book_id,))

    # Fetch the results
    result = cursor.fetchone()

    # Print the book details
    if result:
        print("Book ID:", result[0])
        print("Title:", result[1])
        print("Author:", result[2])
        print("ISBN:", result[3])
        print("Status:", result[4])

        if result[5] is not None:
            print("Reserved by:")
            print("User ID:", result[5])
            print("Reservation Date:", result[6])
            print("User Name:", result[7])
            print("User Email:", result[8])
    else:
        print("Book not found.")

    # Close the connection
    connection.close()

# Function to find a book's reservation status based on BookID, Title, UserID, and ReservationID
def find_reservation_status(identifier):
    # Connect to the database
    connection = sqlite3.connect('library.db')

    # Check the identifier type based on its prefix
    if identifier[:2] == 'LB':
        # BookID
        cursor = connection.execute("SELECT Status FROM Books WHERE BookID = ?", (identifier,))
    elif identifier[:2] == 'LU':
        # UserID
        cursor = connection.execute("SELECT Books.Status FROM Books INNER JOIN Reservations ON "
                                    "Books.BookID = Reservations.BookID WHERE Reservations.UserID = ?", (identifier,))
    elif identifier[:2] == 'LR':
        # ReservationID
        cursor = connection.execute("SELECT Books.Status FROM Books INNER JOIN Reservations ON "
                                    "Books.BookID = Reservations.BookID WHERE Reservations.ReservationID = ?", (identifier,))
    else:
        # Title
        cursor = connection.execute('''SELECT Books.BookID, Books.Title, Books.Author, Books.ISBN, Books.Status,
                                             Reservations.UserID, Reservations.ReservationDate,
                                             Users.Name, Users.Email
                                      FROM Books
                                      LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                                      LEFT JOIN Users ON Reservations.UserID = Users.UserID
                                      WHERE Books.Title = ?''', (identifier,))

    # Fetch the results
    results = cursor.fetchall()

    # Print the reservation status
    if results:
        for result in results:
            if result[5] is None:
                print("Book ID:", result[0])
                print("Title:", result[1])
                print("Author:", result[2])
                print("ISBN:", result[3])
                print("Status:", result[4])
                print("Reservation: Not reserved")
            else:
                print("Book ID:", result[0])
                print("Title:", result[1])
                print("Author:", result[2])
                print("ISBN:", result[3])
                print("Status:", result[4])
                print("Reserved by:")
                print("User ID:", result[5])
                print("Reservation Date:", result[6])
                print("User Name:", result[7])
                print("User Email:", result[8])
    else:
        print("Book not found.")

    # Close the connection
    connection.close()

# Function to find all the books in the database
def find_all_books():
    # Connect to the database
    connection = sqlite3.connect('library.db')

    # Retrieve all the books using JOIN
    cursor = connection.execute('''SELECT Books.BookID, Books.Title, Books.Author, Books.ISBN, Books.Status,
                                     Reservations.UserID, Reservations.ReservationDate,
                                     Users.Name, Users.Email
                                  FROM Books
                                  LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                                  LEFT JOIN Users ON Reservations.UserID = Users.UserID''')

    # Fetch the results
    results = cursor.fetchall()

    # Print the book details
    if results:
        for result in results:
            print("Book ID:", result[0])
            print("Title:", result[1])
            print("Author:", result[2])
            print("ISBN:", result[3])
            print("Status:", result[4])

            if result[5] is not None:
                print("Reserved by:")
                print("User ID:", result[5])
                print("Reservation Date:", result[6])
                print("User Name:", result[7])
                print("User Email:", result[8])
    else:
        print("No books found.")

    # Close the connection
    connection.close()

# Function to modify/update book details based on BookID
def modify_book(book_id):
    # Connect to the database
    connection = sqlite3.connect('library.db')

    # Get input from the user
    new_status = input("Enter the new status for the book: ")

    # Update the book status in the Books table
    connection.execute("UPDATE Books SET Status = ? WHERE BookID = ?", (new_status, book_id))

    # Update the book status in the Reservations table
    connection.execute("UPDATE Reservations SET ReservationDate = NULL WHERE BookID = ?", (book_id,))

    # Commit the changes and close the connection
    connection.commit()
    connection.close()

# Function to delete a book based on its BookID
def delete_book(book_id):
    # Connect to the database
    connection = sqlite3.connect('library.db')

    # Check if the book is reserved
    cursor = connection.execute("SELECT * FROM Reservations WHERE BookID = ?", (book_id,))
    if cursor.fetchone():
        # Book is reserved, delete from both Books and Reservations tables
        connection.execute("DELETE FROM Books WHERE BookID = ?", (book_id,))
        connection.execute("DELETE FROM Reservations WHERE BookID = ?", (book_id,))
    else:
        # Book is not reserved, delete only from the Books table
        connection.execute("DELETE FROM Books WHERE BookID = ?", (book_id,))

    # Commit the changes and close the connection
    connection.commit()
    connection.close()

# Main program loop
def main():
    # Create the database and tables
    create_database()

    while True:
        # Display menu options
        print("--- Library Management System ---")
        print("1. Add a new book")
        print("2. Find a book's details")
        print("3. Find a book's reservation status")
        print("4. Find all books")
        print("5. Modify book details")
        print("6. Delete a book")
        print("7. Exit")

        # Get user's choice
        choice = input("Enter your choice: ")

        if choice == "1":
            add_book()
        elif choice == "2":
            book_id = input("Enter the BookID: ")
            find_book_details(book_id)
        elif choice == "3":
            identifier = input("Enter BookID, UserID, ReservationID, or Title: ")
            find_reservation_status(identifier)
        elif choice == "4":
            find_all_books()
        elif choice == "5":
            book_id = input("Enter the BookID to modify: ")
            modify_book(book_id)
        elif choice == "6":
            book_id = input("Enter the BookID to delete: ")
            delete_book(book_id)
        elif choice == "7":
            print("Exiting the program...")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the main program
if __name__ == "__main__":
    main()