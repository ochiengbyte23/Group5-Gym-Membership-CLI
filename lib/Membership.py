class Membership:
    PLANS = {
        "bronze":  {"duration": "1 month",   "price": 5000},
        "silver":  {"duration": "3 months",  "price": 8000},
        "gold":    {"duration": "6 months",  "price": 15000},
        "diamond": {"duration": "12 months", "price": 30000},
    }

    def __init__(self, membership_plan="none"):
        self.membership_plan = membership_plan

    def add_plan(self, plan):
        if plan in self.PLANS:
            self.membership_plan = plan
            return True
        return False

    def plan_upgrade(self, new_plan):
        return self.add_plan(new_plan)

    def cancel_plan(self):
        self.membership_plan = "none"

    def __str__(self):
        if self.membership_plan == "none":
            return "No active plan"
        info = self.PLANS[self.membership_plan]
        return f"{self.membership_plan.title()} - {info['duration']}  Ksh{info['price']:,}"