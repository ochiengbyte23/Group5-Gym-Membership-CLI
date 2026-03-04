import argparse
import os
import json

from lib.Admin import Admin
from lib.Membership import Membership
from lib.Trainer import Trainer
from lib.User import User

#________file path using os and json__________
DATA_DIR = 'data'
USERS_FILE = os.path.join(DATA_DIR, 'users.json')
TRAINERS_FILE = os.path.join(DATA_DIR, 'trainers.json')
MEMBERSHIPS_FILE = os.path.join(DATA_DIR, 'memberships.json')
ADMIN_FILE = os.path.join(DATA_DIR, 'admin.json')

os.makedirs(DATA_DIR, exist_ok=True)

#__________file I/O helpers___________
def load(path):
    try:
        with open(path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f'{path} not found in folder')
        return []
    
def save(path, data):
    with open(path, 'w') as file:
        json.dump(data, file, indent=2)
        
#_________smart counter_______________
def next_id(records):
    return max((r["id"] for r in records), default = 0) + 1

#______________User commands_______________
def add_user(args):
    users = load(USERS_FILE)
    user = User(next_id(users), args.name, args.email)
    users.append(user.to_dict())
    save(USERS_FILE, users)
    print(f"User added: {user}")

def list_users(args):
    users = load(USERS_FILE)
    if not users:
        print("No users found.")
        return
    for u in users:
        print(f"  [{u['id']}] {u['name']} | {u['email']} | Plan: {u['membership_plan']}")
        
#________________Trainer commands________________________
def add_trainer(args):
    trainers = load(TRAINERS_FILE)
    trainer = Trainer(next_id(trainers), args.name, args.experience)
    trainers.append(trainer.to_dict())
    save(TRAINERS_FILE, trainers)
    print(f"Trainer added: {trainer}")

def list_trainers(args):
    trainers = load(TRAINERS_FILE)
    if not trainers:
        print("No trainers found.")
        return
    for t in trainers:
        print(f"  [{t['id']}] {t['name']} | Experience: {t['experience']} yrs | Trainees: {t['trainees_id']}")
        
#______________Membership commands_______________________________
def upgrade_membership(args):
    users = load(USERS_FILE)
    user = next((u for u in users if u["id"] == args.user_id), None)
    if not user:
        print(f"User ID {args.user_id} not found.")
        return
    valid = ["bronze", "silver", "gold", "diamond"]
    if args.plan not in valid:
        print(f"Invalid plan. Choose from: {valid}")
        return
    user["membership_plan"] = args.plan
    save(USERS_FILE, users)
    
    admin_records = load(ADMIN_FILE)
    for r in admin_records:
     if r["user_id"] == args.user_id:
        r["status"] = args.plan
    save(ADMIN_FILE, admin_records)
    
    print(f"User {user['name']} upgraded to {args.plan} plan.")

def cancel_membership(args):
    users = load(USERS_FILE)
    user = next((u for u in users if u["id"] == args.user_id), None)
    if not user:
        print(f"User ID {args.user_id} not found.")
        return
    user["membership_plan"] = "none"
    save(USERS_FILE, users)
    
    admin_records = load(ADMIN_FILE)
    for r in admin_records:
        if r["user_id"] == args.user_id:
            r["status"] = "none"
    save(ADMIN_FILE, admin_records)
    
    print(f"Membership cancelled for {user['name']}.")

#___________Admin commands(booking)_________
def book_trainer(args):
    users = load(USERS_FILE)
    trainers = load(TRAINERS_FILE)
    admin_records = load(ADMIN_FILE)
    
    user = next((u for u in users if u['id'] == args.user_id), None)
    trainer = next((t for t in trainers if t['id'] == args.trainer_id), None)
    
    if not user:
        print(f'User ID {args.user_id} not found.')
        return
    if not trainer:
        print(f"Trainer ID {args.trainer_id} not found.")
        return
    
    # links user to trainers in trainees list(users)
    if args.user_id not in trainer['trainees_id']:
        trainer['trainees_id'].append(args.user_id)
        save(TRAINERS_FILE, trainers)
        
    record = Admin(
    admin_id=next_id(admin_records),          
    trainer_id=args.trainer_id,
    user_id=args.user_id,
    schedule=args.schedule,
    status=user["membership_plan"]
    )
    admin_records.append(record.to_dict())
    save(ADMIN_FILE, admin_records)
    print(f"{user['name']} booked trainer {trainer['name']} at {args.schedule}.")
    
 #__________listing schedule_____________________   
def list_schedules(args):
    admin_records = load(ADMIN_FILE)
    users = load(USERS_FILE)
    trainers = load(TRAINERS_FILE)

    if not admin_records:
        print("No bookings found.")
        return
    
    for r in admin_records:
        uname = next((u["name"] for u in users if u["id"] == r["user_id"]), "?")
        tname = next((t["name"] for t in trainers if t["id"] == r["trainer_id"]), "?")
        print(f"  [{r['id']}] {uname} → Trainer: {tname} | {r['schedule']} | Status: {r['status']}")
        
        
        
def main():
        parser = argparse.ArgumentParser(prog="gym", description="Gym Membership CLI")
        sub = parser.add_subparsers(dest="command", metavar="COMMAND",)
        
          # add-user
        p = sub.add_parser("add-user", help="name email")
        p.add_argument("name")
        p.add_argument("email")
        p.set_defaults(func=add_user)

        # list-users
        p = sub.add_parser("list-users", help="List all users")
        p.set_defaults(func=list_users)

        # add-trainer
        p = sub.add_parser("add-trainer", help="name\t" "experience")
        p.add_argument("name")
        p.add_argument("experience", type=int)
        p.set_defaults(func=add_trainer)

        # list-trainers
        p = sub.add_parser("list-trainers", help="List all trainers")
        p.set_defaults(func=list_trainers)

        # upgrade-membership
        p = sub.add_parser("upgrade-membership", help="add user_id and plan(bronze, silver, gold, diamond)")
        p.add_argument("user_id", type=int)
        p.add_argument("plan", choices=["bronze", "silver", "gold", "diamond"])
        p.set_defaults(func=upgrade_membership)

        # cancel-membership
        p = sub.add_parser("cancel-membership", help="Cancel a user's membership")
        p.add_argument("user_id", type=int)
        p.set_defaults(func=cancel_membership)

        # book-trainer
        p = sub.add_parser("book-trainer", help=" add user_id, trainer_id and schedule")
        p.add_argument("user_id", type=int, help="e.g. 1")
        p.add_argument("trainer_id", type=int)
        p.add_argument("schedule", help='Session time e.g. "Mon 09:00"')
        p.set_defaults(func=book_trainer)

        # list-schedules
        p = sub.add_parser("list-schedules", help="List all trainer bookings")
        p.set_defaults(func=list_schedules)

        args = parser.parse_args()
        
        if args.command:
            args.func(args)
        else:
            parser.print_help()

if __name__ == "__main__":
    main()
