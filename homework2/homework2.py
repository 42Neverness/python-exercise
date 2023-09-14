import sqlite3

# Function to create the SQLite database and table
def create_database_and_table():
    conn = sqlite3.connect("stephen_king_adaptations.db")
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS stephen_king_adaptations_table (
                      movieID TEXT PRIMARY KEY,
                      movieName TEXT,
                      movieYear INTEGER,
                      imdbRating REAL)''')

    conn.commit()
    conn.close()

# Function to read the file and copy content to a list
def read_file_and_copy_to_list(filename):
    with open(filename, 'r') as file:
        return file.readlines()

# Function to insert data from the list into the database
def insert_data_into_database(data_list):
    conn = sqlite3.connect("stephen_king_adaptations.db")
    cursor = conn.cursor()

    for line in data_list:
        movie_data = line.strip().split(',')
        if len(movie_data) == 4:  # Ensure the line has four elements
            cursor.execute("INSERT INTO stephen_king_adaptations_table (movieID, movieName, movieYear, imdbRating) VALUES (?, ?, ?, ?)",
                           (movie_data[0], movie_data[1], int(movie_data[2]), float(movie_data[3])))

    conn.commit()
    conn.close()

# Function to search for movies in the database based on user input
def search_movies_in_database():
    conn = sqlite3.connect("stephen_king_adaptations.db")
    cursor = conn.cursor()

    while True:
        print("\nOptions:")
        print("1. Search by Movie Name")
        print("2. Search by Movie Year")
        print("3. Search by Movie Rating")
        print("4. STOP")
        choice = input("Enter your choice: ")

        if choice == '1':
            movie_name = input("Enter the name of the movie: ")
            cursor.execute("SELECT * FROM stephen_king_adaptations_table WHERE movieName=?", (movie_name,))
            result = cursor.fetchone()
            if result:
                print("Movie ID:", result[0])
                print("Movie Name:", result[1])
                print("Movie Year:", result[2])
                print("IMDB Rating:", result[3])
            else:
                print("No such movie exists in our database.")
        elif choice == '2':
            year = input("Enter the year: ")
            cursor.execute("SELECT * FROM stephen_king_adaptations_table WHERE movieYear=?", (year,))
            results = cursor.fetchall()
            if results:
                for result in results:
                    print("Movie ID:", result[0])
                    print("Movie Name:", result[1])
                    print("Movie Year:", result[2])
                    print("IMDB Rating:", result[3])
            else:
                print("No movies were found for that year in our database.")
        elif choice == '3':
            rating = float(input("Enter the minimum rating: "))
            cursor.execute("SELECT * FROM stephen_king_adaptations_table WHERE imdbRating >= ?", (rating,))
            results = cursor.fetchall()
            if results:
                for result in results:
                    print("Movie ID:", result[0])
                    print("Movie Name:", result[1])
                    print("Movie Year:", result[2])
                    print("IMDB Rating:", result[3])
            else:
                print("No movies at or above that rating were found in the database.")
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please enter a valid option.")

    conn.close()

if __name__ == "__main__":
    create_database_and_table()
    file_data = read_file_and_copy_to_list("stephen_king_adaptations.txt")
    insert_data_into_database(file_data)
    search_movies_in_database()
