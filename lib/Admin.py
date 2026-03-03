class Admin:
    admin_list = []
    def __init__(self, admin_id, schedule, trainer_id, user_id, status = "none"):
        self.admin_id = admin_id
        self.schedule = schedule
        self.trainer_id = trainer_id
        self.user_id = user_id
        self.status = status
        Admin.admin_list.append(self)
        
    def scheduling_day(self):
            return self.schedule
        
    def no_members(self):
            return len(self.admin_list)
        
    def to_dict(self):
            return {
               "id": self.admin_id ,
               "trainer_id": self.trainer_id, 
               "user_id": self.user_id,
               "schedule": self.schedule,
               "status": self.status,
            }
            
    def __str__(self):
        return f'Booking({self.admin_id }) User: {self.user_id} Trainer {self.trainer_id} at {self.schedule}'
      
        