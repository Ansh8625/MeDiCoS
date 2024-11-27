import mysql.connector

# Connect to MySQL
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Replace with your MySQL username
        password="8625",  # Replace with your MySQL password
        database="MedicalStore"
    )

# Login system
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
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Perform login
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
            print(f"\nLogin successful! Welcome, {role}.")
            if role == "Admin":
                admin_block()
            elif role == "Customer":
                customer_block()
        else:
            print("Invalid username or password. Please try again.")
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

        print("\n--- Create Account ---")
        username = input("Enter a username: ")
        password = input("Enter a password: ")
        role = input("Enter role (Admin/Customer): ").capitalize()

        if role not in ['Admin', 'Customer']:
            print("Invalid role. Please choose 'Admin' or 'Customer'.")
            return

        query = "INSERT INTO Users (username, password, role) VALUES (%s, %s, %s)"
        cursor.execute(query, (username, password, role))
        db.commit()
        print(f"Account created successfully for {role}: {username}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        db.close()

# Admin functionalities
def admin_block():
    while True:
        print("\n--- Admin Block ---")
        print("1. Add Medicine")
        print("2. View Medicines")
        print("3. Update Medicine Stock")
        print("4. Delete Medicine")
        print("5. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_medicine()
        elif choice == "2":
            view_medicines()
        elif choice == "3":
            update_stock()
        elif choice == "4":
            delete_medicine()
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")

def add_medicine():
    try:
        db = connect_to_db()
        cursor = db.cursor()

        name = input("Enter medicine name: ")
        quantity = int(input("Enter quantity: "))
        price = float(input("Enter price per unit: "))

        query = "INSERT INTO Medicines (name, quantity, price) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, quantity, price))
        db.commit()

        print(f"{name} added successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        db.close()

def view_medicines():
    try:
        db = connect_to_db()
        cursor = db.cursor()

        cursor.execute("SELECT * FROM Medicines")
        medicines = cursor.fetchall()

        print("\nAvailable Medicines:")
        for med in medicines:
            print(f"ID: {med[0]}, Name: {med[1]}, Quantity: {med[2]}, Price: {med[3]}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        db.close()

def update_stock():
    db = connect_to_db()
    cursor = db.cursor()
    
    view_medicines()
    med_id = int(input("Enter medicine ID to update: "))
    new_quantity = int(input("Enter new quantity: "))
    
    query = "UPDATE Medicines SET quantity = %s WHERE medicine_id = %s"  # Use correct column name
    cursor.execute(query, (new_quantity, med_id))
    db.commit()
    
    print("Stock updated successfully!")
    cursor.close()
    db.close()


def delete_medicine():
    try:
        db = connect_to_db()
        cursor = db.cursor()

        view_medicines()
        med_id = int(input("Enter medicine ID to delete: "))

        query = "DELETE FROM Medicines WHERE id = %s"
        cursor.execute(query, (med_id,))
        db.commit()

        print("Medicine deleted successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        db.close()

# Customer functionalities
def customer_block():
    while True:
        print("\n--- Customer Block ---")
        print("1. View Medicines")
        print("2. Buy Medicine")
        print("3. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            view_medicines()
        elif choice == "2":
            buy_medicine()
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

def buy_medicine():
    db = connect_to_db()
    cursor = db.cursor()
    
    view_medicines()
    med_id = int(input("Enter medicine ID to buy: "))
    quantity = int(input("Enter quantity to purchase: "))
    
    # Check availability (update column name from 'id' to correct one, e.g., 'medicine_id')
    cursor.execute("SELECT * FROM Medicines WHERE medicine_id = %s", (med_id,))
    medicine = cursor.fetchone()
    
    if medicine and medicine[2] >= quantity:
        total_price = quantity * medicine[3]
        
        # Update stock
        new_quantity = medicine[2] - quantity
        cursor.execute("UPDATE Medicines SET quantity = %s WHERE medicine_id = %s", (new_quantity, med_id))
        
        # Record sale
        cursor.execute("INSERT INTO Sales (medicine_name, quantity, total_price) VALUES (%s, %s, %s)", 
                       (medicine[1], quantity, total_price))
        
        db.commit()
        print(f"{quantity} units of {medicine[1]} purchased successfully! Total price: ₹{total_price}")
    else:
        print("Insufficient stock or invalid medicine ID.")
    
    cursor.close()
    db.close()


# Main function
def main():
    print("\n--- Welcome to the Medical Store Management System ---")
    login()

if __name__ == "__main__":
    main()
