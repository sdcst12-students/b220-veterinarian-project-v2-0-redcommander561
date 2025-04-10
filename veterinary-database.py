import sqlite3
import tkinter


class database:
    def __init__(self, db='dbase.db'):
        self.file = db
        self.connection = sqlite3.connect(self.file)
        self.cursor = self.connection.cursor()
        
        self.table()
    
    def table(self):

        self.cursor.execute("drop table if exists customers")
        self.cursor.execute("""
        create table if not exists customers (
            id integer primary key autoincrement,
            fname text,
            lname text,
            phoneNum text,
            email text,
            address text, 
            city text,
            postalcode text
        );
        """)

        self.cursor.execute("drop table if exists pets")
        self.cursor.execute("""
        create table if not exists pets (
            id integer primary key autoincrement,
            pname text,
            type text,
            breed text,
            birthdate text,
            ownerID int,
            foreign key (ownerID) references customers(id)
        );
        """)

        self.cursor.execute("drop table if exists visits")
        self.cursor.execute("""
        create table if not exists visits (
            id integer primary key autoincrement,
            ownerid int,
            petid int,
            details text,
            cost int,
            paid int,
            foreign key (ownerid) references customers(id),
            foreign key (petid) references pets(id)
        );
        """)
        print("Tables created")

    def add(self):
        print("Add a customer:")
        fname = input("First name: ")
        lname = input("Last name: ")
        phone = input("Phone number: ")
        email = input("Email: ")
        address = input("Address: ")
        city = input("City: ")
        postal = input("Postal code: ")

        data = (fname, lname, phone, email, address, city, postal)

        query = f"""insert into customers (fname, lname, phoneNum, email, address, city, postalcode) 
        values ('{data[0]}', '{data[1]}', '{data[2]}', '{data[3]}', '{data[4]}', '{data[5]}', '{data[6]}')
        """

        self.cursor.execute(query)
        for i in data:
            print(i)
        self.connection.commit()

    def search(self):
        field = input("Search by (fname, lname, phoneNum, email): ")
        value = input(f"Enter the {field}: ")

        self.cursor.execute(f"select * from customers where {field} = ?", (value,))
        results = self.cursor.fetchall()

        if results:
            for row in results:
                print(row)
        else:
            print("No customer found.")

    def edit(self):
        self.search()
        cus = input("Enter the ID of the customer to edit: ")
        field = input("Which field to update (fname, lname, phoneNum, email): ")
        new = input(f"Enter the new value for {field}: ")

        self.cursor.execute(f"update customers set {field} = ? where id = ?", (new, cus))
        self.connection.commit()
        print("Customer updated successfully!")

    def close_connection(self):
        self.connection.close()
        print("Connection closed.")

    def menu(self):
        while True:
            print("\n1. Add Customer")
            print("2. Search Customer")
            print("3. Edit Customer")
            print("4. Exit")

            choice = input("Choose an option: ")

            if choice == "1":
                self.add()
            elif choice == "2":
                self.search()
            elif choice == "3":
                self.edit()
            elif choice == "4":
                self.close_connection()
                break
            else:
                print("Invalid option, try again, with only 1, 2, 3, or 4")


if __name__ == "__main__":
    db = database()
    db.menu()
