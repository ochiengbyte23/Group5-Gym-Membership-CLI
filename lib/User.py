class User:
    def __init__(self, user_id, name, email, membership_plan="none"):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.membership_plan = membership_plan

    def user_sign_in(self, name, email):
        return self.name == name and self.email == email

    def changing_membership(self, new_plan):
        self.membership_plan = new_plan

    def book_trainer(self, trainer_id):
        return {"user_id": self.user_id, "trainer_id": trainer_id}

    def to_dict(self):
        return {
            "id": self.user_id,
            "name": self.name,
            "email": self.email,
            "membership_plan": self.membership_plan,
        }

    def __str__(self):
        return f"User({self.user_id}) {self.name} | {self.email} | Plan: {self.membership_plan}"