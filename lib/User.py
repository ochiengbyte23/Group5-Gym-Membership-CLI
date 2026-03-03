class User:
    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.membership = None
        self.trainer = None

    def user_sign_in(self, name, email):
        """Validates the user's credentials and signs them in."""
        if self.name == name and self.email == email:
            print(f"Welcome back, {self.name}! You have successfully signed in.")
            return True
        else:
            print("Sign in failed. Name or email does not match our records.")
            return False

    def changing_membership(self, new_plan):
        """Updates the user's membership plan."""
        valid_plans = ["bronze", "silver", "gold", "diamond"]
        if new_plan.lower() not in valid_plans:
            print(f"Invalid plan '{new_plan}'. Choose from: {', '.join(valid_plans)}.")
            return False
        old_plan = self.membership if self.membership else "None"
        self.membership = new_plan.lower()
        print(f"Membership updated from '{old_plan}' to '{self.membership}' for user {self.name}.")
        return True

    def book_trainer(self, trainer_id):
        """Books a trainer for the user by storing their trainer ID."""
        if self.trainer is not None:
            print(f"You already have trainer ID {self.trainer} booked. Cancel them first to book a new one.")
            return False
        self.trainer = trainer_id
        print(f"Trainer ID {trainer_id} successfully booked for {self.name}.")
        return True

    def cancel_trainer(self):
        """Cancels the user's currently booked trainer."""
        if self.trainer is None:
            print("You have no trainer booked to cancel.")
            return False
        print(f"Trainer ID {self.trainer} booking cancelled for {self.name}.")
        self.trainer = None
        return True

    def get_details(self):
        """Prints a summary of the user's current details."""
        print(f"--- User Details ---")
        print(f"  ID         : {self.user_id}")
        print(f"  Name       : {self.name}")
        print(f"  Email      : {self.email}")
        print(f"  Membership : {self.membership if self.membership else 'None'}")
        print(f"  Trainer ID : {self.trainer if self.trainer else 'None'}")
        print(f"--------------------")

    def __str__(self):
        return f"User({self.user_id}, {self.name}, {self.email})"