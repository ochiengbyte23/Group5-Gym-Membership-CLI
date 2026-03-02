class Membership:
    """
    So this class is going to represent the membership plans and operations
    Available plans:
    - Bronze: Ksh. 5,000 per month
    - Silver: Ksh 10,000 every 3 months
    - Gold Ksh. 15,000 every 6 months
    - Diamond: Ksh. 30,000 per year
    """
    # Just the basic class constants for the plans
    BRONZE = "Bronze"
    SILVER = "Silver"
    GOLD = "Gold"
    DIAMOND = "Diamond"
    
    # Here what we're doing is just setting up the pricing of the plans
    Prices = {
        BRONZE: 5000,
        SILVER: 10000,
        GOLD: 15000,
        DIAMOND: 30000
    }
    
    # Variable to track the memberships
    all_memberships = []
    
    def __init__(self, membership_id, user_id, membership_plan):
        """
        Initialising a new membership
        
        Arguments:
        membership_id (int): Just a unique membership identifier
        user_id (int): This would be the ID of the user who owns the membership
        membership_plan (str): The plan types (Bronze, Silver, etc)
        """
        self.membership_id = membership_id
        self.user_id = user_id
        self.membership_plan = membership_plan
        self.is_active = True # This will help us track if the membership is active or not
        self.price = self.Prices.get(membership_plan, 0) # This will get the price based on the plan, default will be 0 if not found
        
        Membership.all_memberships.append(self) # Adding the new membership to the list of all memberships
        
        @property
        def membership_plan(self):
            """This is just going to get the current membership plan of the user"""
            return self._membership_plan
        
        @membership_plan.setter
        def membership_plan(self, new_plan):
            """
            Sets a new membership plan WITH validation
            
            Arguments:
            new_plan (str): New plan tpye you want to set it as
            
            Raises:
            Value_error: If the plan type isn't valid
            """
            if new_plan not in self.Prices:
                raise ValueError(f"Invalid membership plan, please choose from: {list(self.Prices.keys())}")
            self._membership_plan = new_plan
            self.price = self.Prices[new_plan] # Now this part updates the price based on the new plan the user chooses
        def add_plan(self, plan_type):
            """
            """
            if plan_type not in self.Prices:
                print(f" Error: Invalid plan type '{plan_type}'")
                print(f"Available plans: {', '.join(self.Prices.keys())}")
                return False 
           
            self.membership_plan = plan_type
            self.is_active = True
            print(f"{plan_type} membership has been activated!!!") 
            print(f" Monthly Cost: Ksh.{self.price}")
            return True
        def plan_upgrade(self):
            pass
        
        def cancel_plan (self):
            pass
         
         