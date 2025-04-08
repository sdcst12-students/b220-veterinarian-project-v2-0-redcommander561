import sqlite3

    
file = 'dbase.db'
connection = sqlite3.connect(file)
print(connection)

cursor = connection.cursor()
cursor.execute("drop table if exists customers")
cursor.execute("drop table if exists pets")
cursor.execute("drop table if exists visits")

cursor = connection.cursor()
query = """
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
"""
cursor.execute(query)
"""---------------------------------"""
cursor = connection.cursor()
query = """
create table if not exists pets (
    id integer primary key autoincrement,
    pname text,
    type text,
    breed text,
    birthdate text,
    ownerID int,
    foreign key (ownerID) references customers(id)
    );
    """
cursor.execute(query)
"""-------------------------------"""
cursor = connection.cursor()
query = """
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
"""
cursor.execute(query)

print("Tables created")

"""-----------------------------"""
print("add a customer")
id = input("ID: ")
fname = input("first name: ")
lname = input("last name: ")
phone = input("phone number: ")
email = input("email: ")
address = input("address: ")
city = input("city: ")
postal = input("postal code: ")

data = (id, fname, lname,phone,email,address,city,postal)


query = f"""
insert into customers (fname, lname, phoneNum, email, address, city, postalcode) 
values ('{data[0]}', '{data[1]}', '{data[2]}', '{data[3]}', '{data[4]}', '{data[5]}', '{data[6]}')
"""

cursor.execute(query)
for i in data:
    print(i)
connection.commit()


def add():
    fname = input("First name: ")
    lname = input("Last name: ")
    phone = input("Phone number: ")
    email = input("Email: ")

    
    cursor.execute(f"insert into customers (fname, lname, phoneNum, email) values ('{fname}', '{lname}', '{phone}', '{email}')")
    connection.commit()
    print("Customer added")


def search():
    field = input("Search by (fname, lname, phoneNum, email): ")
    value = input(f"Enter the {field}: ")

    
    cursor.execute(f"select * from customers where {field} = '{value}'")
    results = cursor.fetchall()

    if results:
        for row in results:
            print(row)
    else:
        print("Invalid probably you typed it in wrong or it doesn't exist.")

def edit():
    search()  

    customer_id = input("Enter the ID of the customer to edit: ")
    field = input("Which field to update (fname, lname, phoneNum, email): ")
    new_value = input(f"Enter the new value for {field}: ")

    
    cursor.execute(f"update customers set {field} = '{new_value}' where id = {customer_id}")
    connection.commit()
    print("Customer updated")


def menu():
    while True:
        print("\n1. Add Customer(type 1)")
        print("2. Search Customer(type 2)")
        print("3. Edit Customer(type 3)")
        print("4. Exit(type 4)")

        choice = input("Choose an option: ")

        if choice == "1":
            add()
        elif choice == "2":
            search()
        elif choice == "3":
            edit()
        elif choice == "4":
            connection.close()
            break
        else:
            print("Invalid, try again.")


menu()