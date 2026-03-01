class Membership:
    """
    So this part is going to represent the membership plans and operations
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
    
    def __init__(self, bronze, silver, gold, diamond, membership_plan):
        self.bronze =bronze
        self.silver = silver
        self.gold = gold
        self.diamond = diamond
        self.membership_plan = membership_plan
        
        def add_plan(self):
            pass
    
        def plan_upgrade(self):
            pass
        
        def cancel_plan (self):
            pass
         
         