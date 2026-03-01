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

        def add_plan(self):
            pass
    
        def plan_upgrade(self):
            pass
        
        def cancel_plan (self):
            pass
         
         