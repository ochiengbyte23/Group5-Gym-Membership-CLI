import argparse
import os
import json

from models.Admin import Admin
from models.Membership import Membership
from models.Trainer import Trainer
from models.User import User

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

#___________Admin commands(booking)_________
def book_trainer(args):
    users = load(USERS_FILE)
    trainers = load(TRAINERS_FILE)
    admin = load(ADMIN_FILE)
    
    user = next((u for u in users if u['id'] == args.user_id), None)
    trainer = next((t for t in trainers if t['id'] == args.trainer_id), None)
    
    if not user:
        print(f'User ID {args.user_id} not found.')
        return
    if not trainer:
        print(f"Trainer ID {args.trainer_id} not found.")
        return
    
    # links user to trainers in trainees list
    if args.user_id not in trainer['trainees_id']:
        trainer['trainees_id'].append(args.user_id)
        save(TRAINERS_FILE, trainers)
        
    record = Admin(
    id=next_id(admin_records),          
    trainer_id=args.trainer_id,
    user_id=args.user_id,
    schedule=args.schedule,
    status=user["membership_plan"]
    )
    print(f"{user['name']} booked trainer {trainer['name']} at {args.schedule}.")