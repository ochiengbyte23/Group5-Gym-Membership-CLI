class Admin:
    #list shows the number of users attached to specific trainee
    admin_list = []
    def __init__(self, admin_id, schedule, trainee_id, user_id, status = "active"):
        self.admin_id = admin_id
        self.schedule = schedule
        self.trainee_id = trainee_id
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
               "trainee_idr": self.trainee_id, 
               "user_id": self.user_id,
               "schedule": self.schedule,
               "status": self.status,
            }
            
    def __str__(self):
        return f'Booking({self.admin_id }) User: {self.user_id} Trainer {self.trainee_id} at {self.schedule}'
      
        