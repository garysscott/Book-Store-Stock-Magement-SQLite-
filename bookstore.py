from tabulate import tabulate

import sqlite3

with sqlite3.connect("ebookstore.db") as db:
    cursor = db.cursor()

# Sub-programs:

# This procedure obtains all the data from the 'books' table in the database.
# Tabulate is used to ensure the data that is output is as readable as possible.
def view_all():
    cursor.execute("SELECT * FROM books")
    x = cursor.fetchall()
    print('''
    ╔══════════════════════════════════════════════════════════════════════╗
    ║                        CURRENT STOCK LEVELS                          ║     
    ╚══════════════════════════════════════════════════════════════════════╝       
        ''')
    print(tabulate(x, headers=("ID", "Title", "Author", "Quantity"),
                   tablefmt="double_grid", numalign="center", stralign="center"))


# This procedure takes in inputs from the user and then adds them to the 'books' table in the database.
# ID in table is set to autoincrement therefore the user does not need to enter this - it will be done automatically.
# A Try / Except method is used on the quantity to ensure that an integer is added.
# Once the data is committed, the view_all() procedure is run so the user can check the data has been added.
def add_new():
        title = input("Please enter the title of the book you wish to add: ")
        author = input("Please enter the author of the book you wish to add: ")

        while True:
            try:
                quantity = int(input("Please enter the quantity of the book you wish to add: "))
                break
            except ValueError:
                print("You are supposed to enter a number.  Try again.")

        cursor.execute("""INSERT INTO books(Title, Author, Qty) VALUES (?, ?, ?)""", (title, author, quantity))
        db.commit()

        print(f"\nThe new book - {title}  - has been added to the database.\n\nPlease check the data entry is correct:")

        view_all()


# Upon the sub-program being run, the user is displayed the current stock list where they will be able to locate
# the relevant ID for the book they wish to edit (which is the primary key in the database).
# The user will then input the ID they require along with the new information they need to edit.
# The database record is then amended with the updated data and the user is prompted to check whether the change
# has been done successfully.
def update():
    print("Please make a note of the ID number of the book you wish to edit from the table below:\n")

    view_all()

    id_no = int(input("Please enter the ID code of the book you wish to edit: "))
    title = input("Please enter the title of the book: ")
    author = input("Please enter the author of the book: ")

    while True:
        try:
            quantity = int(input("Please enter the quantity of the book: "))
            break
        except ValueError:
            print("You are supposed to enter a number.  Try again.")

    cursor.execute("UPDATE books SET Title = ?, Author = ?, Qty = ? WHERE ID = ?", (title, author, quantity, id_no))
    db.commit()

    print(f"\nThe book - {title}  - has been edited.\n\nPlease check the data entry is correct:")

    view_all()


# This sub-program (like update()) fiorstly displays the contents of the database so the user can locate the ID
# number of the record they wish to delete.
# The user is then promopted to enter the ID number and then the record is deleted from the books table.
# The view_all() procedure is then run so the user can check the record has been deleted.
def delete():
    print("Please make a note of the ID number of the book you wish to delete from the table below:\n")

    view_all()

    del_no = int(input("Please enter the ID code of the book you wish to delete: "))
    cursor.execute("DELETE FROM books WHERE id = ?", (del_no,))
    db.commit()

    print(f"\nThe book with the code:{del_no}  has been deleted.\n\nPlease check it has been removed:")

    view_all()



# This procedure will search for a code or book title to see if it is stored in the books table.
# Firstly the user will be presented with a menu with three options.  The user must choose the option they require.
# The user is prompted to enter the ID number or title of the book they wish to search for (depending on their choice).
# The books table is search and if the ID or title can be found it is returned.
# If the return is empty then the book is not stored in the books table.
# Tabulate has been used to ensure the search result is as readable as possible.
def search():
    while True:
        try:
            choice = int(input('''
            ╔══════════════════════════════════════════════════╗
            ║               BOOKSTORE STOCK SEARCH             ║
            ╠══════════════════════════════════════════════════╣
            ║ Select an option from the menu below:            ║     
            ╠══════════════════════════════════════════════════╣
            ║   1 ► Search using an ID Number                  ║ 
            ║   2 ► Search for a title                         ║ 
            ║   3 ► Return to the main menu                    ║ 
            ╠══════════════════════════════════════════════════╣
            ║ Enter your choice below:                         ║     
            ╚══════════════════════════════════════════════════╝
            ►►► 
            '''))

            if choice == 1:
                try:
                    book_code = int(input("Please enter the title of the book you wish to search for: "))
                    print("\nPlease note: If the search returns a blank result then the book is not in stock.")

                    cursor.execute("SELECT * FROM books WHERE id = ?", [book_code])
                    info = cursor.fetchall()

                    print('''
╔══════════════════════════════════════════════════════════════╗
║                       SEARCH RESULT                          ║     
╚══════════════════════════════════════════════════════════════╝       
                                                ''')
                    print(tabulate(info, headers=("ID", "Title", "Author", "Quantity"),
                                   tablefmt="double_grid", numalign="center", stralign="center"))
                except ValueError:
                    print("You have to enter integers (numbers).  Please try again.")

            elif choice == 2:
                book_name = input("Please enter the title of the book you wish to search for: ")
                print("\nPlease note: If the search returns a blank result then the book is not in stock.")

                cursor.execute("SELECT * FROM books WHERE Title = ?", [book_name])
                info = cursor.fetchall()

                print('''
╔══════════════════════════════════════════════════════════════╗
║                       SEARCH RESULT                          ║     
╚══════════════════════════════════════════════════════════════╝       
                            ''')
                print(tabulate(info, headers=("ID", "Title", "Author", "Quantity"),
                               tablefmt="double_grid", numalign="center", stralign="center"))

            elif choice == 3:
                break

        except ValueError:
            print("You have to select 1, 2 or 3.  Please try again.")


# Main Program:

while True:
    try:
        menu_choice = int(input('''
            ╔══════════════════════════════════════════════════╗
            ║         BOOKSTORE STOCK MANAGEMENT SYSTEM        ║
            ╠══════════════════════════════════════════════════╣
            ║ Select an option from the menu below:            ║     
            ╠══════════════════════════════════════════════════╣
            ║   1 ► View all books in stock                    ║ 
            ║   2 ► Add a new book to the database             ║ 
            ║   3 ► Update book information                    ║ 
            ║   4 ► Delete a book from the database            ║ 
            ║   5 ► Search the database for a book             ║ 
            ║   6 ► Exit the system                            ║
            ╠══════════════════════════════════════════════════╣
            ║ Enter your choice below:                         ║     
            ╚══════════════════════════════════════════════════╝
            ►►► 
        '''))

        if menu_choice == 1:
            view_all()
        elif menu_choice == 2:
            add_new()
        elif menu_choice == 3:
            update()
        elif menu_choice == 4:
            delete()
        elif menu_choice == 5:
            search()
        elif menu_choice == 6:
            exit()
        else:
            print("\n\t\tYou need to enter a number between 1 and 6.\n\t\tTry again!")

    except ValueError:
        print("\n\t\tYou need to enter a number between 1 and 6.\n\t\tTry again!")


