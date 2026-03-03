class Trainer:
    def __init__(self, trainer_id, name, experience, trainees_id=None):
        self.trainer_id = trainer_id
        self.name = name
        self.experience = experience
        self.trainees_id = trainees_id or []

    def add_user_to_list(self, user_id):
        if user_id not in self.trainees_id:
            self.trainees_id.append(user_id)

    def to_dict(self):
        return {
            "id": self.trainer_id,
            "name": self.name,
            "experience": self.experience,
            "trainees_id": self.trainees_id,
        }

    def __str__(self):
        return f"Trainer({self.trainer_id}) {self.name} | {self.experience} yrs exp"