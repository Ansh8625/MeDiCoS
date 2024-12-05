import mysql.connector

# Connect to MySQL server
def connect_to_server():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="8625"
    )

# Connect to the database
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="8625",
        database="MedicalStore"
    )

# Setup the database and tables
def setup_database():
    try:
        db = connect_to_server()
        cursor = db.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS MedicalStore")
        db.close()

        db = connect_to_db()
        cursor = db.cursor()

        # Create Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(50) NOT NULL,
                role ENUM('Admin', 'Customer') NOT NULL
            )
        """)

        # Create Medicines table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Medicines (
                medicine_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                quantity INT NOT NULL,
                price FLOAT NOT NULL
            )
        """)

        # Create Sales table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Sales (
                sale_id INT AUTO_INCREMENT PRIMARY KEY,
                medicine_name VARCHAR(100) NOT NULL,
                quantity INT NOT NULL,
                total_price FLOAT NOT NULL,
                sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("Database setup complete!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        db.close()

# Login functionality
def login():
    while True:
        print("\n--- Login Menu ---")
        print("1. Login")
        print("2. Create Account")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            perform_login()
        elif choice == "2":
            create_account()
        elif choice == "3":
            exit()
        else:
            print("Invalid choice. Please try again.")

# Perform login process
def perform_login():
    try:
        db = connect_to_db()
        cursor = db.cursor()

        username = input("Enter username: ")
        password = input("Enter password: ")

        query = "SELECT role FROM Users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()

        if result:
            role = result[0]
            print(f"\nLogin successful! Welcome, {username}.")
            if role == "Admin":
                admin_block()
            elif role == "Customer":
                customer_block()
        else:
            print("Invalid username or password.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        db.close()

# Create a new account
def create_account():
    try:
        db = connect_to_db()
        cursor = db.cursor()

        username = input("Enter a username: ")
        password = input("Enter a password: ")
        role = input("Enter role (Admin/Customer): ").capitalize()

        if role not in ['Admin', 'Customer']:
            print("Invalid role. Please enter 'Admin' or 'Customer'.")
            return

        query = "INSERT INTO Users (username, password, role) VALUES (%s, %s, %s)"
        cursor.execute(query, (username, password, role))
        db.commit()
        print("Account created successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        db.close()

# Admin functionalities
def admin_block():
    while True:
        print("\n--- Admin Menu ---")
        print("1. Add Medicine")
        print("2. View Medicines")
        print("3. Delete Medicine")
        print("4. Update Stock")
        print("5. View Sales")
        print("6. Logout")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_medicine()
        elif choice == "2":
            view_medicines()
        elif choice == "3":
            delete_medicine()
        elif choice == "4":
            update_stock()
        elif choice == "5":
            view_sales()
        elif choice == "6":
            logout()
        else:
            print("Invalid choice. Please try again.")

# Customer functionalities
def customer_block():
    while True:
        print("\n--- Customer Menu ---")
        print("1. Buy Medicine")
        print("2. View Available Medicines")
        print("3. Logout")
        choice = input("Enter your choice: ")

        if choice == "1":
            buy_medicine()
        elif choice == "2":
            view_medicines()
        elif choice == "3":
            logout()
        else:
            print("Invalid choice. Please try again.")

# Add medicine to the database
def add_medicine():
    try:
        db = connect_to_db()
        cursor = db.cursor()

        name = input("Enter medicine name: ")
        quantity = int(input("Enter quantity: "))
        price = float(input("Enter price: "))

        query = "INSERT INTO Medicines (name, quantity, price) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, quantity, price))
        db.commit()
        print("Medicine added successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        db.close()

# View medicines
def view_medicines():
    try:
        db = connect_to_db()
        cursor = db.cursor()

        cursor.execute("SELECT * FROM Medicines")
        results = cursor.fetchall()

        print("\n--- Medicines Available ---")
        if results:
            for row in results:
                print(f"ID: {row[0]}, Name: {row[1]}, Quantity: {row[2]}, Price: {row[3]}")
        else:
            print("No medicines available.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        db.close()

# Delete medicine
def delete_medicine():
    try:
        db = connect_to_db()
        cursor = db.cursor()

        med_id = int(input("Enter the ID of the medicine to delete: "))
        query = "DELETE FROM Medicines WHERE medicine_id = %s"
        cursor.execute(query, (med_id,))
        db.commit()

        if cursor.rowcount:
            print("Medicine deleted successfully.")
        else:
            print("Medicine not found.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        db.close()

# Update stock of medicine
def update_stock():
    try:
        db = connect_to_db()
        cursor = db.cursor()

        med_id = int(input("Enter medicine ID: "))
        new_quantity = int(input("Enter new quantity: "))

        query = "UPDATE Medicines SET quantity = %s WHERE medicine_id = %s"
        cursor.execute(query, (new_quantity, med_id))
        db.commit()

        if cursor.rowcount:
            print("Stock updated successfully.")
        else:
            print("Medicine not found.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        db.close()

# Buy medicine
def buy_medicine():
    try:
        db = connect_to_db()
        cursor = db.cursor()

        med_id = int(input("Enter medicine ID to buy: "))
        quantity = int(input("Enter quantity: "))

        query = "SELECT name, price, quantity FROM Medicines WHERE medicine_id = %s"
        cursor.execute(query, (med_id,))
        result = cursor.fetchone()

        if result:
            name, price, available_quantity = result
            if available_quantity >= quantity:
                total_price = quantity * price

                query = "INSERT INTO Sales (medicine_name, quantity, total_price) VALUES (%s, %s, %s)"
                cursor.execute(query, (name, quantity, total_price))
                db.commit()

                query = "UPDATE Medicines SET quantity = %s WHERE medicine_id = %s"
                cursor.execute(query, (available_quantity - quantity, med_id))
                db.commit()

                print(f"Medicine purchased! Total price: {total_price}")
            else:
                print("Not enough stock available.")
        else:
            print("Medicine not found.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        db.close()

# Sales Report
def view_sales():
    try:
        db = connect_to_db()
        cursor = db.cursor()

        # Fetching all columns from Sales table
        cursor.execute("SELECT medicine_name, quantity, total_price FROM Sales")
        results = cursor.fetchall()

        print("\n--- Sales Report ---")
        print(f"{'Medicine':<20} {'Quantity':<10} {'Total Price':<15}")
        print("-" * 55)

        # Check if results exist
        if results:
            for sale in results:
                # sale is a tuple with three elements
                print(f"{sale[0]:<20} {sale[1]:<10} ₹{sale[2]:<15.2f}")
        else:
            print("No sales records found.")
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
    except IndexError as e:
        print("Data Access Error:", e)
    finally:
        cursor.close()
        db.close()


# Logout function
def logout():
    print("Logged out successfully!")
    exit()

# Main function
def main():
    setup_database()
    login()

if __name__ == "__main__":
    main()
