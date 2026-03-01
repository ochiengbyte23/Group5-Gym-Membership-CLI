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
        
      
        