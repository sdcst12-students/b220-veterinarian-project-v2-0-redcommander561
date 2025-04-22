
import sqlite3

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
        print("\n")
        results = []  

        if field in ["fname", "lname", "phoneNum", "phonenum", "email"]:
            value = input(f"Enter the {field}: ")
            self.cursor.execute(f"select * from customers where {field} = ?", (value,))

            results = self.cursor.fetchall()
            if results:
                for row in results:
                    print(row)
            else:
                print("No customer found. Either you typed it in wrong, it doesn't exist or you entered a foreign symbol.\n")

        if field not in ["fname", "lname", "phoneNum", "email"]:
                print("Invalid field entered. ")
                return

        
    def edit(self):
        try:
            self.search()  
            cus = input("Enter the ID of the customer to edit: ")
            
            if not cus:
                print("Invalid ID entered. Please enter a numeric ID.")
                return
            cus = int(cus)
            self.cursor.execute("select * from customers where id = ?", (cus,))
            customer = self.cursor.fetchone()
            if not customer:
                print("Customer not found with that ID.")
                return

            field = input("Which field to update (fname, lname, phoneNum, email): ")

            if field not in ["fname", "lname", "phoneNum", "email"]:
                print("Invalid field entered. ")
                return

            new = input(f"Enter the new value for {field}: ")

            if not new:
                print(f"New value for {field} cannot be empty.")
                return

            query = f"update customers set {field} = ? where id = ?"
            self.cursor.execute(query, (new, cus))
            self.connection.commit()

            print("Customer updated successfully!")

        except Exception as e:
            print(f"Error while updating customer: {e}")


    def close(self):
        self.connection.close()
        print("Program Exited.")

    def menu(self):
        while True:
            print("\n1. Add Customer (type 1)")
            print("2. Search Customer (type 2)")
            print("3. Edit Customer (type 3)")
            print("4. Exit (type 4)")

            choice = input("Choose an option: ")

            if choice == "1" or choice == "Add customer" or choice == "add customer":
                self.add()
            elif choice == "2" or choice == "Search customer" or choice == "search customer":
                self.search()
            elif choice == "3" or choice == "Edit customer" or choice == "edit customer":
                self.edit()
            elif choice == "4" or choice == "exit" or choice == "Exit":
                self.close()
                break
            else:
                print("Invalid option, try again, with only 1, 2, 3, or 4")


if __name__ == "__main__":
    db = database()
    db.menu()


