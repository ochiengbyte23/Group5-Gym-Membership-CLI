import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))
from lib.Admin import Admin
from lib.Membership import Membership
from lib.Trainer import Trainer
from utils.storage import save_data, load_data

def main_menu():
    """Main CLI entry point for the Gym Management System."""
    while True:
        print("\n=== GYM MANAGEMENT SYSTEM ===")
        print("1. Admin Portal\n2. Member Management\n3. Trainer Management\n4. Exit")
        
        choice = input("Select an option (1-4): ")
        if choice == '1': 
            admin_menu()
        elif choice == '2': 
            member_management_menu()
        elif choice == '3': 
            trainer_management_menu()
        elif choice == '4': 
            print("Thank you for using the Gym Management System. Goodbye!")
            break
        else: 
            print("Invalid selection. Please try again.")

def admin_menu():
    """Sub-menu for Admin-related actions."""
    print("\n--- Admin Portal ---")
    print("1. Manage Members\n2. Manage Trainers\n3. Back to Main Menu")
    
    sub_choice = input("Select an option: ")
    if sub_choice == '1': 
        print("Admin managing members...")
        member_management_menu()  # Redirect to member management
    elif sub_choice == '2':
        print("Admin managing trainers...")
        trainer_management_menu()  # Redirect to trainer management
    elif sub_choice == '3':
        return
    else:
        print("Invalid selection.")

def member_management_menu():
    """Sub-menu for Member-related actions."""
    print("\n--- Member Management ---")
    print("1. Register Member\n2. View Members\n3. Back to Main Menu")
    choice = input("Select an option: ")
    
    if choice == '1':
        name = input("Enter member name: ")
        email = input("Enter member email: ")
        
        # Load existing members first
        members = load_data("members.json")
        
        # Create a new User instance
        user_id = len(members) + 1  # Simple ID generation
        new_member = Membership(name, email, user_id)
        
        # Add to list and save
        members.append({
            "name": new_member.name,
            "email": new_member.email,
            "user_id": new_member.user_id
        })
        save_data("members.json", members)
        print(f"Member {name} registered successfully with ID: {user_id}")
        
    elif choice == '2':
        print("\nMember List:")
        # Load members from JSON and display
        members = load_data("members.json")
        if members:
            for member in members:
                print(f"ID: {member['user_id']}, Name: {member['name']}, Email: {member['email']}")
        else:
            print("No members found.")
    elif choice == '3':
        return
    else:
        print("Invalid selection.")

def trainer_management_menu():
    """Sub-menu for Trainer-related actions."""
    print("\n--- Trainer Management ---")
    print("1. Add Trainer\n2. View Trainers\n3. Back to Main Menu")
    choice = input("Select an option: ")
    
    if choice == '1':
        name = input("Enter trainer name: ")
        trainer_id = input("Enter trainer ID: ")
        experience = input("Enter trainer experience: ")
        
        # Create trainer instance
        trainer = Trainer(name, trainer_id, experience)
        
        # Load existing trainers
        trainers = load_data("trainers.json")
        
        # Add trainer to list
        trainer_dict = {
            "name": name,
            "trainer_id": trainer_id,
            "experience": experience
        }
        trainers.append(trainer_dict)
        save_data("trainers.json", trainers)
        print(f"Trainer {name} added successfully.")
        
    elif choice == '2':
        print("\nTrainer List:")
        # Load trainers from JSON and display
        trainers = load_data("trainers.json")
        if trainers:
            for trainer in trainers:
                print(f"ID: {trainer['trainer_id']}, Name: {trainer['name']}, Experience: {trainer['experience']} years")
        else:
            print("No trainers found.")
    elif choice == '3':
        return
    else:
        print("Invalid selection.")

if __name__ == "__main__":
    # Create data directory if it doesn't exist
    if not os.path.exists('data'):
        os.makedirs('data')
    main_menu()